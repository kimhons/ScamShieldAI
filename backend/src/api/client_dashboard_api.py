#!/usr/bin/env python3
"""
ScamShield AI Client Dashboard API
Comprehensive backend API for client dashboard functionality
"""

import os
import json
import uuid
import asyncio
import hashlib
import mimetypes
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

from flask import Flask, request, jsonify, send_file, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import threading
import time
from pathlib import Path

# Import our API integrations
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from integrations.api_manager import APIManager
    from reports.simplified_report_engine import ReportEngine
    from services.payment_service import PaymentService
except ImportError as e:
    print(f"Warning: Could not import some modules: {e}")
    # Create mock classes for development
    class APIManager:
        def __init__(self):
            pass
        async def investigate_email(self, email): return {"risk_score": 0.3, "status": "safe"}
        async def investigate_phone(self, phone): return {"risk_score": 0.2, "status": "safe"}
        async def investigate_domain(self, domain): return {"risk_score": 0.4, "status": "suspicious"}
        async def investigate_ip(self, ip): return {"risk_score": 0.1, "status": "safe"}
        async def investigate_url(self, url): return {"risk_score": 0.5, "status": "malicious"}
    
    class ReportEngine:
        def __init__(self):
            pass
        def generate_report(self, data, template="professional"): 
            return {"report_id": "RPT-" + str(uuid.uuid4())[:8], "status": "completed"}
    
    class PaymentService:
        def __init__(self):
            pass
        def process_payment(self, amount, method="stripe"): 
            return {"payment_id": "PAY-" + str(uuid.uuid4())[:8], "status": "completed"}

# Enums and Data Classes
class InvestigationType(Enum):
    EMAIL = "email"
    PHONE = "phone"
    NAME = "name"
    DOMAIN = "domain"
    SOCIAL = "social"

class InvestigationLevel(Enum):
    BASIC = "basic"
    STANDARD = "standard"
    PROFESSIONAL = "professional"
    FORENSIC = "forensic"

class InvestigationStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class User:
    user_id: str
    email: str
    name: str
    password_hash: str
    membership_type: str = "basic"
    created_at: datetime = None
    last_login: datetime = None
    total_spent: float = 0.0
    reports_generated: int = 0
    threats_detected: int = 0

@dataclass
class Investigation:
    investigation_id: str
    user_id: str
    target_type: str
    target_value: str
    investigation_level: str
    status: str
    price: float
    created_at: datetime
    completed_at: Optional[datetime] = None
    evidence_files: List[str] = None
    evidence_links: List[Dict] = None
    additional_notes: str = ""
    results: Optional[Dict] = None
    report_path: Optional[str] = None

@dataclass
class EvidenceFile:
    file_id: str
    investigation_id: str
    filename: str
    file_type: str
    file_size: int
    upload_path: str
    uploaded_at: datetime

# Flask App Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'scamshield-dev-key-2024')
app.config['UPLOAD_FOLDER'] = '/tmp/scamshield_uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

CORS(app, supports_credentials=True)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Setup
DATABASE_PATH = '/tmp/scamshield_client.db'

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            membership_type TEXT DEFAULT 'basic',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            total_spent REAL DEFAULT 0.0,
            reports_generated INTEGER DEFAULT 0,
            threats_detected INTEGER DEFAULT 0
        )
    ''')
    
    # Investigations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investigations (
            investigation_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            target_type TEXT NOT NULL,
            target_value TEXT NOT NULL,
            investigation_level TEXT NOT NULL,
            status TEXT NOT NULL,
            price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            evidence_files TEXT,
            evidence_links TEXT,
            additional_notes TEXT,
            results TEXT,
            report_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Evidence files table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evidence_files (
            file_id TEXT PRIMARY KEY,
            investigation_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            upload_path TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (investigation_id) REFERENCES investigations (investigation_id)
        )
    ''')
    
    # Sessions table for user sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize services
api_manager = APIManager()
report_engine = ReportEngine()
payment_service = PaymentService()

# Pricing configuration
PRICING = {
    "basic": {"price": 9.99, "features": ["Essential fraud detection", "24-hour delivery", "PDF report"]},
    "standard": {"price": 24.99, "features": ["Comprehensive analysis", "12-hour delivery", "Multiple formats"]},
    "professional": {"price": 49.99, "features": ["Expert analysis", "6-hour delivery", "All formats", "Phone support"]},
    "forensic": {"price": 99.99, "features": ["Court-ready documentation", "3-hour delivery", "Expert testimony"]}
}

# Helper Functions
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def generate_id(prefix=""):
    """Generate unique ID with optional prefix"""
    return f"{prefix}{uuid.uuid4().hex[:8].upper()}"

def allowed_file(filename):
    """Check if file type is allowed"""
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'mp4', 'zip'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Authentication Endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        name = data.get('name', '').strip()
        password = data.get('password', '')
        
        if not all([email, name, password]):
            return jsonify({"error": "Email, name, and password are required"}), 400
        
        # Check if user already exists
        conn = get_db_connection()
        existing_user = conn.execute('SELECT user_id FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            conn.close()
            return jsonify({"error": "User already exists"}), 409
        
        # Create new user
        user_id = generate_id("USR-")
        password_hash = generate_password_hash(password)
        
        conn.execute('''
            INSERT INTO users (user_id, email, name, password_hash, membership_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, email, name, password_hash, "premium"))
        
        conn.commit()
        conn.close()
        
        # Create session
        session['user_id'] = user_id
        session['email'] = email
        session['name'] = name
        
        return jsonify({
            "message": "Registration successful",
            "user": {
                "user_id": user_id,
                "email": email,
                "name": name,
                "membership_type": "premium"
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        if not all([email, password]):
            return jsonify({"error": "Email and password are required"}), 400
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if not user or not check_password_hash(user['password_hash'], password):
            conn.close()
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Update last login
        conn.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?', (user['user_id'],))
        conn.commit()
        conn.close()
        
        # Create session
        session['user_id'] = user['user_id']
        session['email'] = user['email']
        session['name'] = user['name']
        
        return jsonify({
            "message": "Login successful",
            "user": {
                "user_id": user['user_id'],
                "email": user['email'],
                "name": user['name'],
                "membership_type": user['membership_type']
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """User logout"""
    session.clear()
    return jsonify({"message": "Logout successful"}), 200

# Dashboard Endpoints
@app.route('/api/dashboard/stats', methods=['GET'])
@require_auth
def get_dashboard_stats():
    """Get user dashboard statistics"""
    try:
        user_id = session['user_id']
        
        conn = get_db_connection()
        
        # Get user stats
        user_stats = conn.execute('''
            SELECT total_spent, reports_generated, threats_detected
            FROM users WHERE user_id = ?
        ''', (user_id,)).fetchone()
        
        # Get recent investigations count
        recent_investigations = conn.execute('''
            SELECT COUNT(*) as count FROM investigations 
            WHERE user_id = ? AND created_at > datetime('now', '-30 days')
        ''', (user_id,)).fetchone()
        
        # Calculate success rate
        total_investigations = conn.execute('''
            SELECT COUNT(*) as total FROM investigations WHERE user_id = ?
        ''', (user_id,)).fetchone()
        
        completed_investigations = conn.execute('''
            SELECT COUNT(*) as completed FROM investigations 
            WHERE user_id = ? AND status = 'completed'
        ''', (user_id,)).fetchone()
        
        conn.close()
        
        success_rate = 100.0
        if total_investigations['total'] > 0:
            success_rate = (completed_investigations['completed'] / total_investigations['total']) * 100
        
        return jsonify({
            "stats": {
                "reports_generated": user_stats['reports_generated'] or 0,
                "total_spent": user_stats['total_spent'] or 0.0,
                "threats_detected": user_stats['threats_detected'] or 0,
                "success_rate": round(success_rate, 1),
                "recent_investigations": recent_investigations['count'] or 0
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get stats: {str(e)}"}), 500

@app.route('/api/dashboard/recent-reports', methods=['GET'])
@require_auth
def get_recent_reports():
    """Get user's recent investigation reports"""
    try:
        user_id = session['user_id']
        limit = request.args.get('limit', 10, type=int)
        
        conn = get_db_connection()
        investigations = conn.execute('''
            SELECT * FROM investigations 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit)).fetchall()
        
        conn.close()
        
        reports = []
        for inv in investigations:
            reports.append({
                "investigation_id": inv['investigation_id'],
                "target_type": inv['target_type'],
                "target_value": inv['target_value'],
                "investigation_level": inv['investigation_level'],
                "status": inv['status'],
                "price": inv['price'],
                "created_at": inv['created_at'],
                "completed_at": inv['completed_at'],
                "has_report": bool(inv['report_path'])
            })
        
        return jsonify({"reports": reports}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get reports: {str(e)}"}), 500

# Investigation Endpoints
@app.route('/api/investigations/create', methods=['POST'])
@require_auth
def create_investigation():
    """Create new investigation"""
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        # Validate required fields
        target_type = data.get('target_type')
        target_value = data.get('target_value', '').strip()
        investigation_level = data.get('investigation_level', 'standard')
        
        if not all([target_type, target_value]):
            return jsonify({"error": "Target type and value are required"}), 400
        
        if target_type not in [e.value for e in InvestigationType]:
            return jsonify({"error": "Invalid target type"}), 400
        
        if investigation_level not in PRICING:
            return jsonify({"error": "Invalid investigation level"}), 400
        
        # Get pricing
        price = PRICING[investigation_level]["price"]
        
        # Create investigation record
        investigation_id = generate_id("RPT-2024-")
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO investigations (
                investigation_id, user_id, target_type, target_value,
                investigation_level, status, price, additional_notes,
                evidence_links
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            investigation_id, user_id, target_type, target_value,
            investigation_level, InvestigationStatus.PENDING.value, price,
            data.get('additional_notes', ''),
            json.dumps(data.get('evidence_links', []))
        ))
        
        conn.commit()
        conn.close()
        
        # Start investigation processing in background
        threading.Thread(
            target=process_investigation_async,
            args=(investigation_id,),
            daemon=True
        ).start()
        
        return jsonify({
            "message": "Investigation created successfully",
            "investigation": {
                "investigation_id": investigation_id,
                "target_type": target_type,
                "target_value": target_value,
                "investigation_level": investigation_level,
                "status": InvestigationStatus.PENDING.value,
                "price": price,
                "estimated_completion": (datetime.now() + timedelta(hours=24)).isoformat()
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Failed to create investigation: {str(e)}"}), 500

@app.route('/api/investigations/<investigation_id>/status', methods=['GET'])
@require_auth
def get_investigation_status(investigation_id):
    """Get investigation status"""
    try:
        user_id = session['user_id']
        
        conn = get_db_connection()
        investigation = conn.execute('''
            SELECT * FROM investigations 
            WHERE investigation_id = ? AND user_id = ?
        ''', (investigation_id, user_id)).fetchone()
        
        if not investigation:
            conn.close()
            return jsonify({"error": "Investigation not found"}), 404
        
        # Get evidence files
        evidence_files = conn.execute('''
            SELECT filename, file_type, file_size, uploaded_at
            FROM evidence_files 
            WHERE investigation_id = ?
        ''', (investigation_id,)).fetchall()
        
        conn.close()
        
        return jsonify({
            "investigation": {
                "investigation_id": investigation['investigation_id'],
                "target_type": investigation['target_type'],
                "target_value": investigation['target_value'],
                "investigation_level": investigation['investigation_level'],
                "status": investigation['status'],
                "price": investigation['price'],
                "created_at": investigation['created_at'],
                "completed_at": investigation['completed_at'],
                "evidence_files": [dict(f) for f in evidence_files],
                "evidence_links": json.loads(investigation['evidence_links'] or '[]'),
                "additional_notes": investigation['additional_notes'],
                "has_report": bool(investigation['report_path']),
                "results": json.loads(investigation['results'] or '{}')
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get investigation status: {str(e)}"}), 500

# Evidence Upload Endpoints
@app.route('/api/investigations/<investigation_id>/upload-evidence', methods=['POST'])
@require_auth
def upload_evidence(investigation_id):
    """Upload evidence files for investigation"""
    try:
        user_id = session['user_id']
        
        # Verify investigation belongs to user
        conn = get_db_connection()
        investigation = conn.execute('''
            SELECT investigation_id FROM investigations 
            WHERE investigation_id = ? AND user_id = ?
        ''', (investigation_id, user_id)).fetchone()
        
        if not investigation:
            conn.close()
            return jsonify({"error": "Investigation not found"}), 404
        
        # Handle file uploads
        uploaded_files = []
        
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400
        
        files = request.files.getlist('files')
        
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                # Secure filename
                filename = secure_filename(file.filename)
                file_id = generate_id("FILE-")
                
                # Create unique filename to avoid conflicts
                file_extension = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{file_id}.{file_extension}"
                
                # Save file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                
                # Get file info
                file_size = os.path.getsize(file_path)
                file_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                
                # Save to database
                conn.execute('''
                    INSERT INTO evidence_files (
                        file_id, investigation_id, filename, file_type,
                        file_size, upload_path
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (file_id, investigation_id, filename, file_type, file_size, file_path))
                
                uploaded_files.append({
                    "file_id": file_id,
                    "filename": filename,
                    "file_type": file_type,
                    "file_size": file_size
                })
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "message": f"Uploaded {len(uploaded_files)} files successfully",
            "files": uploaded_files
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to upload evidence: {str(e)}"}), 500

@app.route('/api/investigations/<investigation_id>/download-report', methods=['GET'])
@require_auth
def download_report(investigation_id):
    """Download investigation report"""
    try:
        user_id = session['user_id']
        
        conn = get_db_connection()
        investigation = conn.execute('''
            SELECT report_path, target_value FROM investigations 
            WHERE investigation_id = ? AND user_id = ? AND status = 'completed'
        ''', (investigation_id, user_id)).fetchone()
        
        conn.close()
        
        if not investigation:
            return jsonify({"error": "Report not found or not ready"}), 404
        
        if not investigation['report_path'] or not os.path.exists(investigation['report_path']):
            return jsonify({"error": "Report file not found"}), 404
        
        return send_file(
            investigation['report_path'],
            as_attachment=True,
            download_name=f"ScamShield_Report_{investigation_id}.pdf"
        )
        
    except Exception as e:
        return jsonify({"error": f"Failed to download report: {str(e)}"}), 500

# Payment Endpoints
@app.route('/api/payment/process', methods=['POST'])
@require_auth
def process_payment():
    """Process payment for investigation"""
    try:
        data = request.get_json()
        investigation_id = data.get('investigation_id')
        payment_method = data.get('payment_method', 'stripe')
        
        if not investigation_id:
            return jsonify({"error": "Investigation ID required"}), 400
        
        user_id = session['user_id']
        
        conn = get_db_connection()
        investigation = conn.execute('''
            SELECT price, status FROM investigations 
            WHERE investigation_id = ? AND user_id = ?
        ''', (investigation_id, user_id)).fetchone()
        
        if not investigation:
            conn.close()
            return jsonify({"error": "Investigation not found"}), 404
        
        if investigation['status'] != 'pending':
            conn.close()
            return jsonify({"error": "Investigation already processed"}), 400
        
        # Process payment
        payment_result = payment_service.process_payment(
            amount=investigation['price'],
            method=payment_method
        )
        
        if payment_result.get('status') == 'completed':
            # Update investigation status
            conn.execute('''
                UPDATE investigations 
                SET status = 'processing' 
                WHERE investigation_id = ?
            ''', (investigation_id,))
            
            # Update user total spent
            conn.execute('''
                UPDATE users 
                SET total_spent = total_spent + ? 
                WHERE user_id = ?
            ''', (investigation['price'], user_id))
            
            conn.commit()
            conn.close()
            
            return jsonify({
                "message": "Payment processed successfully",
                "payment_id": payment_result.get('payment_id'),
                "investigation_status": "processing"
            }), 200
        else:
            conn.close()
            return jsonify({"error": "Payment failed"}), 400
        
    except Exception as e:
        return jsonify({"error": f"Payment processing failed: {str(e)}"}), 500

# Pricing Endpoint
@app.route('/api/pricing', methods=['GET'])
def get_pricing():
    """Get pricing information"""
    return jsonify({"pricing": PRICING}), 200

# Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ScamShield AI Client Dashboard API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }), 200

# Background Processing Functions
def process_investigation_async(investigation_id):
    """Process investigation in background"""
    try:
        time.sleep(2)  # Simulate initial processing delay
        
        conn = get_db_connection()
        investigation = conn.execute('''
            SELECT * FROM investigations WHERE investigation_id = ?
        ''', (investigation_id,)).fetchone()
        
        if not investigation:
            conn.close()
            return
        
        # Update status to analyzing
        conn.execute('''
            UPDATE investigations 
            SET status = 'analyzing' 
            WHERE investigation_id = ?
        ''', (investigation_id,))
        conn.commit()
        
        # Simulate investigation processing
        target_type = investigation['target_type']
        target_value = investigation['target_value']
        
        # Run actual investigation using API manager
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            if target_type == 'email':
                results = loop.run_until_complete(api_manager.investigate_email(target_value))
            elif target_type == 'phone':
                results = loop.run_until_complete(api_manager.investigate_phone(target_value))
            elif target_type == 'domain':
                results = loop.run_until_complete(api_manager.investigate_domain(target_value))
            else:
                results = {"risk_score": 0.3, "status": "analyzed", "details": "Investigation completed"}
        except Exception as e:
            results = {"error": str(e), "risk_score": 0.0, "status": "error"}
        finally:
            loop.close()
        
        # Simulate processing time based on investigation level
        processing_times = {"basic": 5, "standard": 8, "professional": 12, "forensic": 15}
        time.sleep(processing_times.get(investigation['investigation_level'], 8))
        
        # Generate report
        report_result = report_engine.generate_report(
            data={
                "investigation_id": investigation_id,
                "target_type": target_type,
                "target_value": target_value,
                "results": results,
                "investigation_level": investigation['investigation_level']
            },
            template=investigation['investigation_level']
        )
        
        # Update investigation with results
        conn.execute('''
            UPDATE investigations 
            SET status = 'completed', 
                completed_at = CURRENT_TIMESTAMP,
                results = ?,
                report_path = ?
            WHERE investigation_id = ?
        ''', (json.dumps(results), report_result.get('report_path'), investigation_id))
        
        # Update user stats
        threats_detected = 1 if results.get('risk_score', 0) > 0.5 else 0
        conn.execute('''
            UPDATE users 
            SET reports_generated = reports_generated + 1,
                threats_detected = threats_detected + ?
            WHERE user_id = ?
        ''', (threats_detected, investigation['user_id']))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        # Mark investigation as failed
        conn = get_db_connection()
        conn.execute('''
            UPDATE investigations 
            SET status = 'failed',
                results = ?
            WHERE investigation_id = ?
        ''', (json.dumps({"error": str(e)}), investigation_id))
        conn.commit()
        conn.close()

# Demo Data Creation
def create_demo_user():
    """Create demo user for testing"""
    try:
        conn = get_db_connection()
        
        # Check if demo user exists
        existing_user = conn.execute('SELECT user_id FROM users WHERE email = ?', ('sarah@demo.com',)).fetchone()
        if existing_user:
            conn.close()
            return existing_user['user_id']
        
        # Create demo user
        user_id = "USR-DEMO001"
        password_hash = generate_password_hash("demo123")
        
        conn.execute('''
            INSERT INTO users (user_id, email, name, password_hash, membership_type, total_spent, reports_generated, threats_detected)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, "sarah@demo.com", "Sarah Johnson", password_hash, "premium", 347.0, 7, 3))
        
        # Create demo investigations
        demo_investigations = [
            {
                "investigation_id": "RPT-2024-001847",
                "target_type": "email",
                "target_value": "john.smith@email.com",
                "investigation_level": "professional",
                "status": "completed",
                "price": 49.99,
                "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "completed_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                "results": json.dumps({"risk_score": 0.2, "status": "safe", "details": "No threats detected"})
            },
            {
                "investigation_id": "RPT-2024-001846",
                "target_type": "phone",
                "target_value": "+1-555-0123",
                "investigation_level": "basic",
                "status": "analyzing",
                "price": 9.99,
                "created_at": (datetime.now() - timedelta(hours=3)).isoformat()
            },
            {
                "investigation_id": "RPT-2024-001845",
                "target_type": "domain",
                "target_value": "suspicious-profile.com",
                "investigation_level": "standard",
                "status": "completed",
                "price": 24.99,
                "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "completed_at": (datetime.now() - timedelta(hours=20)).isoformat(),
                "results": json.dumps({"risk_score": 0.8, "status": "suspicious", "details": "Domain flagged for suspicious activity"})
            }
        ]
        
        for inv in demo_investigations:
            conn.execute('''
                INSERT INTO investigations (
                    investigation_id, user_id, target_type, target_value,
                    investigation_level, status, price, created_at,
                    completed_at, results
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                inv["investigation_id"], user_id, inv["target_type"], inv["target_value"],
                inv["investigation_level"], inv["status"], inv["price"], inv["created_at"],
                inv.get("completed_at"), inv.get("results")
            ))
        
        conn.commit()
        conn.close()
        
        return user_id
        
    except Exception as e:
        print(f"Error creating demo user: {e}")
        return None

# Demo login endpoint
@app.route('/api/auth/demo-login', methods=['POST'])
def demo_login():
    """Demo login for testing"""
    try:
        user_id = create_demo_user()
        if not user_id:
            return jsonify({"error": "Failed to create demo user"}), 500
        
        # Create session
        session['user_id'] = user_id
        session['email'] = "sarah@demo.com"
        session['name'] = "Sarah Johnson"
        
        return jsonify({
            "message": "Demo login successful",
            "user": {
                "user_id": user_id,
                "email": "sarah@demo.com",
                "name": "Sarah Johnson",
                "membership_type": "premium"
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Demo login failed: {str(e)}"}), 500

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Create demo user
    create_demo_user()
    
    print("🚀 ScamShield AI Client Dashboard API starting...")
    print("📊 Dashboard API: http://localhost:5007")
    print("🔐 Demo Login: POST /api/auth/demo-login")
    print("📈 Health Check: GET /api/health")
    print("💰 Pricing: GET /api/pricing")
    
    app.run(host='0.0.0.0', port=5007, debug=True)

