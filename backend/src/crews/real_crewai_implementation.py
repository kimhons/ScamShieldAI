"""
ScamShield AI - Real CrewAI Implementation

This module implements actual CrewAI agents and crews to replace
the simulated agents, providing live multi-agent investigations.
"""

import os
import sys
import yaml
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai.memory import LongTermMemory
from crewai_tools import BaseTool

# ScamShield imports
from config.llm_config import get_agent_llm, get_crew_manager_llm
from tools.scamshield_tools import (
    WhoisDomainLookup, DNSAnalysis, SSLCertificateAnalysis,
    EmailHeaderAnalysis, EmailReputation, AuthenticationCheck,
    SanctionsScreening, FinancialIntelligence, AMLAnalysis,
    BlockchainAnalysis, WalletClustering, CryptoCompliance,
    ThreatAssessment, AttributionAnalysis, StrategicIntelligence,
    SignalsIntelligence, CommunicationAnalysis, PatternAnalysis
)
from memory.investigation_memory import InvestigationMemory

logger = logging.getLogger(__name__)

class RealCrewAIImplementation:
    """Real CrewAI implementation for ScamShield AI investigations"""
    
    def __init__(self):
        """Initialize the real CrewAI implementation"""
        self.config_dir = Path(__file__).parent.parent / "agents" / "config"
        self.agents_config = self._load_config("agents.yaml")
        self.tasks_config = self._load_config("tasks.yaml")
        self.memory = InvestigationMemory()
        self.tools = self._initialize_tools()
        self.agents = {}
        self.crews = {}
        
        logger.info("🚀 Real CrewAI implementation initialized")
    
    def _load_config(self, filename: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_path = self.config_dir / filename
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                logger.info(f"✅ Loaded configuration from {filename}")
                return config
        except Exception as e:
            logger.error(f"❌ Failed to load {filename}: {e}")
            return {}
    
    def _initialize_tools(self) -> Dict[str, BaseTool]:
        """Initialize all available tools"""
        tools = {
            # Domain and DNS tools
            'whois_domain_lookup': WhoisDomainLookup(),
            'dns_analysis': DNSAnalysis(),
            'ssl_certificate_analysis': SSLCertificateAnalysis(),
            
            # Email tools
            'email_header_analysis': EmailHeaderAnalysis(),
            'email_reputation': EmailReputation(),
            'authentication_check': AuthenticationCheck(),
            
            # Financial intelligence tools
            'sanctions_screening': SanctionsScreening(),
            'financial_intelligence': FinancialIntelligence(),
            'aml_analysis': AMLAnalysis(),
            
            # Cryptocurrency tools
            'blockchain_analysis': BlockchainAnalysis(),
            'wallet_clustering': WalletClustering(),
            'crypto_compliance': CryptoCompliance(),
            
            # Threat assessment tools
            'threat_assessment': ThreatAssessment(),
            'attribution_analysis': AttributionAnalysis(),
            'strategic_intelligence': StrategicIntelligence(),
            
            # Signals intelligence tools
            'signals_intelligence': SignalsIntelligence(),
            'communication_analysis': CommunicationAnalysis(),
            'pattern_analysis': PatternAnalysis()
        }
        
        logger.info(f"🔧 Initialized {len(tools)} investigation tools")
        return tools
    
    def create_agent(self, agent_name: str, agent_config: Dict[str, Any]) -> Agent:
        """Create a CrewAI agent from configuration"""
        try:
            # Get agent-specific LLM
            llm = get_agent_llm(agent_name)
            
            # Get tools for this agent
            agent_tools = []
            if 'tools' in agent_config:
                for tool_name in agent_config['tools']:
                    if tool_name in self.tools:
                        agent_tools.append(self.tools[tool_name])
                    else:
                        logger.warning(f"⚠️ Tool {tool_name} not found for agent {agent_name}")
            
            # Create agent
            agent = Agent(
                role=agent_config['role'],
                goal=agent_config['goal'],
                backstory=agent_config['backstory'],
                tools=agent_tools,
                llm=llm,
                memory=agent_config.get('memory', True),
                verbose=agent_config.get('verbose', True),
                max_iter=agent_config.get('max_iter', 10),
                max_rpm=agent_config.get('max_rpm', 30),
                allow_delegation=agent_config.get('allow_delegation', False)
            )
            
            logger.info(f"✅ Created agent: {agent_name}")
            return agent
            
        except Exception as e:
            logger.error(f"❌ Failed to create agent {agent_name}: {e}")
            raise
    
    def create_task(self, task_name: str, task_config: Dict[str, Any], agent: Agent, context: Dict[str, Any] = None) -> Task:
        """Create a CrewAI task from configuration"""
        try:
            # Format description and expected output with context
            description = task_config['description']
            expected_output = task_config['expected_output']
            
            if context:
                description = description.format(**context)
                expected_output = expected_output.format(**context)
            
            # Get tools for this task
            task_tools = []
            if 'tools' in task_config:
                for tool_name in task_config['tools']:
                    if tool_name in self.tools:
                        task_tools.append(self.tools[tool_name])
            
            task = Task(
                description=description,
                expected_output=expected_output,
                agent=agent,
                tools=task_tools
            )
            
            logger.info(f"✅ Created task: {task_name}")
            return task
            
        except Exception as e:
            logger.error(f"❌ Failed to create task {task_name}: {e}")
            raise
    
    def create_investigation_crew(self, investigation_type: str, target: str) -> Crew:
        """Create a specialized investigation crew"""
        try:
            crew_agents = []
            crew_tasks = []
            
            # Context for task formatting
            context = {
                'target': target,
                'domain': target if '.' in target else '',
                'email': target if '@' in target else '',
                'entity': target,
                'crypto_address': target if len(target) > 25 else ''
            }
            
            # Define investigation workflows based on type
            if investigation_type == 'domain':
                workflow = ['fbi_cyber_specialist', 'domain_specialist']
                task_sequence = ['domain_investigation', 'threat_assessment']
            elif investigation_type == 'email':
                workflow = ['email_specialist', 'fbi_cyber_specialist']
                task_sequence = ['email_investigation', 'threat_assessment']
            elif investigation_type == 'financial':
                workflow = ['cia_intelligence_analyst', 'financial_analyst']
                task_sequence = ['financial_intelligence', 'threat_assessment']
            elif investigation_type == 'crypto':
                workflow = ['crypto_specialist', 'cia_intelligence_analyst']
                task_sequence = ['cryptocurrency_investigation', 'financial_intelligence']
            elif investigation_type == 'comprehensive':
                workflow = [
                    'fbi_cyber_specialist', 'cia_intelligence_analyst',
                    'mi6_signals_specialist', 'mossad_counterintel_specialist'
                ]
                task_sequence = [
                    'domain_investigation', 'financial_intelligence',
                    'signals_analysis', 'threat_assessment', 'comprehensive_report'
                ]
            else:
                # Default comprehensive investigation
                workflow = ['fbi_cyber_specialist', 'cia_intelligence_analyst']
                task_sequence = ['domain_investigation', 'threat_assessment']
            
            # Create agents
            for agent_name in workflow:
                if agent_name in self.agents_config:
                    agent = self.create_agent(agent_name, self.agents_config[agent_name])
                    crew_agents.append(agent)
                    self.agents[agent_name] = agent
            
            # Create tasks
            for i, task_name in enumerate(task_sequence):
                if task_name in self.tasks_config and i < len(crew_agents):
                    task = self.create_task(
                        task_name, 
                        self.tasks_config[task_name], 
                        crew_agents[i % len(crew_agents)],
                        context
                    )
                    crew_tasks.append(task)
            
            # Create crew with hierarchical process for complex investigations
            process = Process.hierarchical if len(crew_agents) > 2 else Process.sequential
            manager_llm = get_crew_manager_llm() if process == Process.hierarchical else None
            
            crew = Crew(
                agents=crew_agents,
                tasks=crew_tasks,
                process=process,
                manager_llm=manager_llm,
                memory=True,
                verbose=True,
                max_rpm=100
            )
            
            crew_id = f"{investigation_type}_{int(datetime.now().timestamp())}"
            self.crews[crew_id] = crew
            
            logger.info(f"🎯 Created {investigation_type} investigation crew with {len(crew_agents)} agents and {len(crew_tasks)} tasks")
            return crew
            
        except Exception as e:
            logger.error(f"❌ Failed to create investigation crew: {e}")
            raise
    
    def execute_investigation(self, target: str, investigation_type: str = "comprehensive", 
                            investigation_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a real CrewAI investigation"""
        try:
            start_time = datetime.now()
            investigation_id = f"INV-{int(start_time.timestamp())}"
            
            logger.info(f"🚀 Starting real CrewAI investigation {investigation_id} for {target}")
            
            # Create investigation crew
            crew = self.create_investigation_crew(investigation_type, target)
            
            # Prepare investigation inputs
            inputs = {
                'target': target,
                'investigation_type': investigation_type,
                'investigation_id': investigation_id,
                'timestamp': start_time.isoformat(),
                'params': investigation_params or {}
            }
            
            # Execute the crew
            logger.info(f"🔄 Executing crew with {len(crew.agents)} agents...")
            result = crew.kickoff(inputs=inputs)
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Process results
            investigation_results = self._process_crew_results(
                result, investigation_id, target, investigation_type, 
                execution_time, len(crew.agents)
            )
            
            # Store in memory
            self.memory.store_investigation(investigation_id, investigation_results)
            
            logger.info(f"✅ Investigation {investigation_id} completed in {execution_time:.2f}s")
            return investigation_results
            
        except Exception as e:
            logger.error(f"❌ Investigation failed: {e}")
            return {
                "investigation_id": f"INV-ERROR-{int(datetime.now().timestamp())}",
                "target": target,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _process_crew_results(self, crew_result: Any, investigation_id: str, target: str, 
                            investigation_type: str, execution_time: float, agents_count: int) -> Dict[str, Any]:
        """Process and format crew execution results"""
        try:
            # Extract results from crew output
            if hasattr(crew_result, 'raw'):
                raw_output = crew_result.raw
            else:
                raw_output = str(crew_result)
            
            # Try to parse as JSON if possible
            try:
                if isinstance(raw_output, str) and raw_output.strip().startswith('{'):
                    parsed_result = json.loads(raw_output)
                else:
                    parsed_result = {"analysis": raw_output}
            except json.JSONDecodeError:
                parsed_result = {"analysis": raw_output}
            
            # Calculate risk level and confidence
            confidence_score = self._calculate_confidence(parsed_result)
            risk_level = self._determine_risk_level(confidence_score, parsed_result)
            
            # Format final results
            investigation_results = {
                "investigation_id": investigation_id,
                "target": target,
                "investigation_type": investigation_type,
                "status": "completed",
                "risk_level": risk_level,
                "confidence_score": round(confidence_score, 3),
                "execution_time": round(execution_time, 2),
                "agents_used": agents_count,
                "crew_results": parsed_result,
                "summary": {
                    "total_findings": len(parsed_result.get('findings', [])),
                    "risk_factors_identified": len(parsed_result.get('risk_factors', [])),
                    "overall_assessment": f"{risk_level} risk with {round(confidence_score * 100, 1)}% confidence"
                },
                "findings": parsed_result.get('findings', [])[:10],
                "risk_factors": parsed_result.get('risk_factors', [])[:8],
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "framework": "CrewAI Multi-Agent System",
                    "version": "1.0.0",
                    "api_version": "2024.1",
                    "real_execution": True
                }
            }
            
            return investigation_results
            
        except Exception as e:
            logger.error(f"❌ Failed to process crew results: {e}")
            return {
                "investigation_id": investigation_id,
                "target": target,
                "status": "processing_error",
                "error": str(e),
                "raw_output": str(crew_result),
                "timestamp": datetime.now().isoformat()
            }
    
    def _calculate_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate confidence score from investigation results"""
        try:
            # Look for confidence indicators in results
            if 'confidence' in results:
                return float(results['confidence'])
            
            # Calculate based on findings and evidence
            findings_count = len(results.get('findings', []))
            risk_factors_count = len(results.get('risk_factors', []))
            
            # Base confidence on amount of evidence
            base_confidence = min(0.9, (findings_count * 0.1) + (risk_factors_count * 0.05))
            
            # Adjust based on result quality
            if 'threat_level' in results:
                base_confidence += 0.1
            if 'attribution' in results:
                base_confidence += 0.1
                
            return min(1.0, max(0.1, base_confidence))
            
        except Exception:
            return 0.75  # Default confidence
    
    def _determine_risk_level(self, confidence: float, results: Dict[str, Any]) -> str:
        """Determine risk level from confidence and results"""
        try:
            risk_factors_count = len(results.get('risk_factors', []))
            threat_indicators = len(results.get('threat_indicators', []))
            
            # Calculate risk score
            risk_score = (confidence * 0.4) + (risk_factors_count * 0.1) + (threat_indicators * 0.15)
            
            if risk_score >= 0.9:
                return "CRITICAL"
            elif risk_score >= 0.7:
                return "HIGH"
            elif risk_score >= 0.4:
                return "MEDIUM"
            else:
                return "LOW"
                
        except Exception:
            return "MEDIUM"  # Default risk level

# Global instance
real_crewai = RealCrewAIImplementation()

# Convenience functions
def execute_real_investigation(target: str, investigation_type: str = "comprehensive", 
                              params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Execute a real CrewAI investigation"""
    return real_crewai.execute_investigation(target, investigation_type, params)

def get_available_agents() -> List[str]:
    """Get list of available agent types"""
    return list(real_crewai.agents_config.keys())

def get_available_investigation_types() -> List[str]:
    """Get list of available investigation types"""
    return ['domain', 'email', 'financial', 'crypto', 'comprehensive']

if __name__ == "__main__":
    # Test the real CrewAI implementation
    print("🧪 Testing Real CrewAI Implementation...")
    
    # Test investigation
    test_target = "suspicious-domain.com"
    result = execute_real_investigation(test_target, "domain")
    
    print(f"Investigation ID: {result.get('investigation_id')}")
    print(f"Status: {result.get('status')}")
    print(f"Risk Level: {result.get('risk_level')}")
    print(f"Confidence: {result.get('confidence_score')}")
    print(f"Execution Time: {result.get('execution_time')}s")

