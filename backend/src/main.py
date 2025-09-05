"""
ScamShield AI - Enhanced Backend Application

Elite fraud investigation platform with hybrid AI capabilities, credit system, and advanced reporting
"""

import os
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import uuid
import json

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import base64

# Import AI Engine components
from ai_engine.investigation_engine import InvestigationEngine, InvestigationRequest, InvestigationType
from ai_engine.model_manager_v2 import ModelTier
from ai_engine.prompt_engineering import prompt_engineer, AnalysisDepth

# Import Credit System components
from models.credit_system import (
    Subscription, CreditTransaction, SubscriptionTier, CreditCalculator,
    InvestigationComplexity, ProcessingPriority
)
from routes.credit_management import credit_bp

# Import Report Generation components
from report_templates.report_generator import (
    ReportGenerator, ReportTier, ReportFormat, ReportStatus
)

# Import Database models
from models.user import db as user_db, User
from models.investigation import Investigation, Report, Evidence, ScamDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'scamshield-ai-secret-key-2025')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///scamshield_ai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Initialize extensions
CORS(app, origins=["*"])
user_db.init_app(app)

# Register blueprints
app.register_blueprint(credit_bp)

# Initialize AI Investigation Engine
investigation_engine = InvestigationEngine()

# Tier pricing configuration
TIER_PRICING = {
    ModelTier.BASIC: {"price": 9.99, "credits": 10, "name": "Basic Scam Detection"},
    ModelTier.PROFESSIONAL: {"price": 49.99, "credits": 25, "name": "Professional Investigation"},
    ModelTier.ENTERPRISE: {"price": 199.99, "credits": 100, "name": "Enterprise Intelligence"},
    ModelTier.INTELLIGENCE: {"price": 499.99, "credits": 250, "name": "Elite Intelligence Analysis"}
}

@app.before_first_request
def create_tables():
    """Create database tables"""
    with app.app_context():
        user_db.create_all()
        logger.info("Database tables created")

# ============ CORE API ENDPOINTS ============

@app.route('/')
def index():
    """Serve the main application"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "2.0.0",
        "ai_engine": "operational"
    })

@app.route('/api/tiers')
def get_tiers():
    """Get available investigation tiers"""
    tiers = []
    for tier, config in TIER_PRICING.items():
        tiers.append({
            "tier": tier.value,
            "name": config["name"],
            "price": config["price"],
            "credits": config["credits"],
            "features": get_tier_features(tier)
        })
    
    return jsonify({"tiers": tiers})

def get_tier_features(tier: ModelTier) -> List[str]:
    """Get features for each tier"""
    features = {
        ModelTier.BASIC: [
            "Quick scam detection",
            "Basic risk assessment",
            "Community database check",
            "Simple fraud patterns",
            "Basic recommendations"
        ],
        ModelTier.PROFESSIONAL: [
            "Advanced AI analysis",
            "Multi-modal artifact analysis",
            "Behavioral profiling",
            "Technical infrastructure analysis",
            "Detailed investigation reports",
            "Priority support"
        ],
        ModelTier.ENTERPRISE: [
            "Elite AI model ensemble",
            "Comprehensive threat intelligence",
            "Strategic attribution analysis",
            "Campaign tracking",
            "Advanced pattern recognition",
            "Custom investigation workflows",
            "API access",
            "Dedicated support"
        ],
        ModelTier.INTELLIGENCE: [
            "Maximum AI capabilities",
            "Real-time threat correlation",
            "Strategic intelligence assessment",
            "Predictive threat modeling",
            "Elite-level analysis depth",
            "Custom AI model training",
            "White-glove service",
            "24/7 expert support"
        ]
    }
    return features.get(tier, [])

# ============ INVESTIGATION ENDPOINTS ============

@app.route('/api/investigate', methods=['POST'])
async def create_investigation():
    """Create a new investigation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['tier', 'artifacts']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Parse tier
        try:
            tier = ModelTier(data['tier'])
        except ValueError:
            return jsonify({"error": "Invalid tier specified"}), 400
        
        # Parse investigation type
        investigation_type = InvestigationType(data.get('investigation_type', 'comprehensive'))
        
        # Generate investigation ID
        investigation_id = str(uuid.uuid4())
        
        # Create investigation request
        investigation_request = InvestigationRequest(
            investigation_id=investigation_id,
            user_id=data.get('user_id', 'anonymous'),
            tier=tier,
            investigation_type=investigation_type,
            artifacts=data['artifacts'],
            context=data.get('context'),
            priority=data.get('priority', 'normal')
        )
        
        # Start investigation (async)
        result = await investigation_engine.conduct_investigation(investigation_request)
        
        # Store investigation in database
        investigation = Investigation(
            id=investigation_id,
            user_id=investigation_request.user_id,
            tier=tier.value,
            status='completed',
            artifacts_count=len(investigation_request.artifacts),
            threat_level=result.threat_level.value,
            confidence_score=result.confidence_score,
            processing_time=result.processing_time,
            cost=result.cost,
            created_at=investigation_request.timestamp,
            completed_at=result.timestamp
        )
        
        user_db.session.add(investigation)
        user_db.session.commit()
        
        # Create investigation report
        report = Report(
            investigation_id=investigation_id,
            executive_summary=result.executive_summary,
            detailed_findings=json.dumps(result.detailed_findings),
            evidence_analysis=json.dumps(result.evidence_analysis),
            recommendations=json.dumps(result.recommendations),
            models_used=json.dumps(result.models_used)
        )
        
        user_db.session.add(report)
        user_db.session.commit()
        
        return jsonify({
            "investigation_id": investigation_id,
            "status": "completed",
            "result": result.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Investigation creation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/investigate/quick', methods=['POST'])
async def quick_investigation():
    """Perform quick investigation for basic tier"""
    try:
        data = request.get_json()
        
        if 'url' not in data and 'content' not in data:
            return jsonify({"error": "URL or content required"}), 400
        
        # Create artifact from input
        if 'url' in data:
            artifact = {"type": "url", "content": data['url']}
        else:
            artifact = {"type": "text", "content": data['content']}
        
        # Create quick investigation request
        investigation_id = str(uuid.uuid4())
        investigation_request = InvestigationRequest(
            investigation_id=investigation_id,
            user_id='anonymous',
            tier=ModelTier.BASIC,
            investigation_type=InvestigationType.QUICK_SCAN,
            artifacts=[artifact]
        )
        
        # Conduct investigation
        result = await investigation_engine.conduct_investigation(investigation_request)
        
        return jsonify({
            "investigation_id": investigation_id,
            "threat_level": result.threat_level.value,
            "confidence_score": result.confidence_score,
            "executive_summary": result.executive_summary,
            "recommendations": result.recommendations[:3],  # Top 3 recommendations
            "processing_time": result.processing_time
        })
        
    except Exception as e:
        logger.error(f"Quick investigation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/investigate/<investigation_id>')
def get_investigation(investigation_id):
    """Get investigation details"""
    try:
        investigation = Investigation.query.filter_by(id=investigation_id).first()
        if not investigation:
            return jsonify({"error": "Investigation not found"}), 404
        
        report = Report.query.filter_by(investigation_id=investigation_id).first()
        
        result = {
            "investigation_id": investigation_id,
            "tier": investigation.tier,
            "status": investigation.status,
            "threat_level": investigation.threat_level,
            "confidence_score": investigation.confidence_score,
            "processing_time": investigation.processing_time,
            "cost": investigation.cost,
            "created_at": investigation.created_at.isoformat(),
            "completed_at": investigation.completed_at.isoformat() if investigation.completed_at else None
        }
        
        if report:
            result.update({
                "executive_summary": report.executive_summary,
                "detailed_findings": json.loads(report.detailed_findings) if report.detailed_findings else {},
                "evidence_analysis": json.loads(report.evidence_analysis) if report.evidence_analysis else {},
                "recommendations": json.loads(report.recommendations) if report.recommendations else [],
                "models_used": json.loads(report.models_used) if report.models_used else []
            })
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Failed to get investigation {investigation_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/investigate/<investigation_id>/status')
def get_investigation_status(investigation_id):
    """Get investigation status"""
    try:
        # Check active investigations first
        status = investigation_engine.get_investigation_status(investigation_id)
        if status:
            return jsonify(status)
        
        # Check database for completed investigations
        investigation = Investigation.query.filter_by(id=investigation_id).first()
        if investigation:
            return jsonify({
                "investigation_id": investigation_id,
                "status": investigation.status,
                "tier": investigation.tier,
                "created_at": investigation.created_at.isoformat()
            })
        
        return jsonify({"error": "Investigation not found"}), 404
        
    except Exception as e:
        logger.error(f"Failed to get investigation status: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ ARTIFACT UPLOAD ENDPOINTS ============

@app.route('/api/upload', methods=['POST'])
def upload_artifact():
    """Upload artifact for investigation"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Secure filename
        filename = secure_filename(file.filename)
        
        # Read file content
        file_content = file.read()
        file_size = len(file_content)
        
        # Determine file type
        file_extension = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        
        # Create artifact object
        artifact = {
            "type": "document" if file_extension in ['pdf', 'doc', 'docx', 'txt'] else "image" if file_extension in ['jpg', 'jpeg', 'png', 'gif'] else "unknown",
            "filename": filename,
            "file_size": file_size,
            "file_type": file_extension,
            "content": base64.b64encode(file_content).decode('utf-8') if file_extension in ['jpg', 'jpeg', 'png', 'gif'] else file_content.decode('utf-8', errors='ignore')
        }
        
        return jsonify({
            "artifact": artifact,
            "message": "File uploaded successfully"
        })
        
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ SCAM DATABASE ENDPOINTS ============

@app.route('/api/scam-database')
def get_scam_database():
    """Get scam database entries"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        query = ScamDatabase.query
        
        if search:
            query = query.filter(
                ScamDatabase.entity_name.contains(search) |
                ScamDatabase.domain.contains(search) |
                ScamDatabase.description.contains(search)
            )
        
        scams = query.order_by(ScamDatabase.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            "scams": [{
                "id": scam.id,
                "entity_name": scam.entity_name,
                "domain": scam.domain,
                "threat_type": scam.threat_type,
                "risk_level": scam.risk_level,
                "description": scam.description,
                "evidence_count": scam.evidence_count,
                "verified": scam.verified,
                "created_at": scam.created_at.isoformat()
            } for scam in scams.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": scams.total,
                "pages": scams.pages,
                "has_next": scams.has_next,
                "has_prev": scams.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get scam database: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/scam-database/<int:scam_id>')
def get_scam_details(scam_id):
    """Get detailed scam information"""
    try:
        scam = ScamDatabase.query.get_or_404(scam_id)
        
        return jsonify({
            "id": scam.id,
            "entity_name": scam.entity_name,
            "domain": scam.domain,
            "threat_type": scam.threat_type,
            "risk_level": scam.risk_level,
            "description": scam.description,
            "indicators": json.loads(scam.indicators) if scam.indicators else [],
            "evidence_count": scam.evidence_count,
            "verified": scam.verified,
            "created_at": scam.created_at.isoformat(),
            "updated_at": scam.updated_at.isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get scam details: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/report-scam', methods=['POST'])
def report_scam():
    """Report a new scam"""
    try:
        data = request.get_json()
        
        required_fields = ['entity_name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new scam report
        scam = ScamDatabase(
            entity_name=data['entity_name'],
            domain=data.get('domain', ''),
            threat_type=data.get('threat_type', 'unknown'),
            risk_level=data.get('risk_level', 'medium'),
            description=data['description'],
            indicators=json.dumps(data.get('indicators', [])),
            evidence_count=data.get('evidence_count', 0),
            verified=False  # Requires manual verification
        )
        
        user_db.session.add(scam)
        user_db.session.commit()
        
        return jsonify({
            "message": "Scam reported successfully",
            "scam_id": scam.id
        })
        
    except Exception as e:
        logger.error(f"Failed to report scam: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ STATISTICS ENDPOINTS ============

@app.route('/api/stats')
def get_statistics():
    """Get platform statistics"""
    try:
        # Investigation statistics
        total_investigations = Investigation.query.count()
        recent_investigations = Investigation.query.filter(
            Investigation.created_at >= datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        
        # Threat level distribution
        threat_levels = user_db.session.query(
            Investigation.threat_level,
            user_db.func.count(Investigation.threat_level)
        ).group_by(Investigation.threat_level).all()
        
        threat_distribution = {level: count for level, count in threat_levels}
        
        # Scam database statistics
        total_scams = ScamDatabase.query.count()
        verified_scams = ScamDatabase.query.filter_by(verified=True).count()
        
        # Tier usage statistics
        tier_usage = user_db.session.query(
            Investigation.tier,
            user_db.func.count(Investigation.tier)
        ).group_by(Investigation.tier).all()
        
        tier_distribution = {tier: count for tier, count in tier_usage}
        
        return jsonify({
            "investigations": {
                "total": total_investigations,
                "today": recent_investigations,
                "threat_distribution": threat_distribution,
                "tier_distribution": tier_distribution
            },
            "scam_database": {
                "total_entries": total_scams,
                "verified_entries": verified_scams,
                "verification_rate": (verified_scams / total_scams * 100) if total_scams > 0 else 0
            },
            "ai_engine": {
                "status": "operational",
                "models_available": len(investigation_engine.model_manager.model_configs),
                "active_investigations": len(investigation_engine.active_investigations)
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get statistics: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ AI MODEL ENDPOINTS ============

@app.route('/api/models')
def get_available_models():
    """Get available AI models"""
    try:
        models = []
        for model_name, config in investigation_engine.model_manager.model_configs.items():
            models.append({
                "name": model_name,
                "type": config.model_type.value,
                "tiers": [tier.value for tier in config.tier_access],
                "capabilities": config.capabilities,
                "cost_per_token": config.cost_per_token,
                "max_tokens": config.max_tokens
            })
        
        return jsonify({"models": models})
        
    except Exception as e:
        logger.error(f"Failed to get models: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

# ============ MAIN APPLICATION ============

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting ScamShield AI Backend on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

