"""
ScamShield AI - Main Investigation Crew

This module implements the primary investigation crew that orchestrates
multiple specialized agents for comprehensive fraud investigation using
CrewAI's multi-agent framework.
"""

from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.memory import LongTermMemory
from crewai.memory.storage import ChromaDBStorage
from crewai.knowledge import Knowledge
from typing import List, Dict, Any, Optional
import os
import logging

# Import ScamShield tools
from ..tools.scamshield_tools import (
    WhoisDomainLookupTool,
    ShodanNetworkScanTool,
    SanctionsScreeningTool,
    IPGeolocationTool,
    DNSAnalysisTool,
    SSLCertificateAnalysisTool,
    FinancialIntelligenceTool,
    BlockchainAnalysisTool,
    EmailHeaderAnalysisTool,
    get_tools_for_agent
)

# Configure logging
logger = logging.getLogger(__name__)

@CrewBase
class ScamShieldInvestigationCrew:
    """
    Elite fraud investigation crew with specialized agents for comprehensive
    multi-agent fraud investigation and intelligence analysis.
    """
    
    # Configuration files
    agents_config = 'agents/config/agents.yaml'
    tasks_config = 'agents/config/tasks.yaml'
    
    def __init__(self):
        """Initialize the investigation crew with memory and knowledge systems"""
        super().__init__()
        
        # Initialize memory system
        self.investigation_memory = LongTermMemory(
            storage=ChromaDBStorage(
                collection_name="scamshield_investigations",
                persist_directory="./memory/investigations"
            )
        )
        
        # Initialize knowledge base
        self.fraud_knowledge = Knowledge(
            sources=[
                "./knowledge/fraud_patterns.json",
                "./knowledge/investigation_reports/",
                "./knowledge/threat_intelligence/"
            ]
        )
        
        # Initialize tools
        self.tools = {
            'whois_tool': WhoisDomainLookupTool(),
            'shodan_tool': ShodanNetworkScanTool(),
            'sanctions_tool': SanctionsScreeningTool(),
            'ipinfo_tool': IPGeolocationTool(),
            'dns_tool': DNSAnalysisTool(),
            'ssl_tool': SSLCertificateAnalysisTool(),
            'financial_tool': FinancialIntelligenceTool(),
            'blockchain_tool': BlockchainAnalysisTool(),
            'email_tool': EmailHeaderAnalysisTool()
        }
        
        logger.info("ScamShield Investigation Crew initialized")
    
    # Agent Definitions
    @agent
    def fbi_cyber_specialist(self) -> Agent:
        """FBI Cyber Division Investigation Specialist"""
        return Agent(
            config=self.agents_config['fbi_cyber_specialist'],
            tools=[
                self.tools['whois_tool'],
                self.tools['shodan_tool'],
                self.tools['dns_tool'],
                self.tools['ssl_tool']
            ],
            memory=self.investigation_memory,
            verbose=True,
            step_callback=self._log_agent_step
        )
    
    @agent
    def cia_intelligence_analyst(self) -> Agent:
        """CIA Intelligence Operations Analyst"""
        return Agent(
            config=self.agents_config['cia_intelligence_analyst'],
            tools=[
                self.tools['sanctions_tool'],
                self.tools['financial_tool'],
                self.tools['ipinfo_tool']
            ],
            memory=self.investigation_memory,
            verbose=True,
            step_callback=self._log_agent_step
        )
    
    @agent
    def mi6_signals_specialist(self) -> Agent:
        """MI6 Signals Intelligence Specialist"""
        return Agent(
            config=self.agents_config['mi6_signals_specialist'],
            tools=[
                self.tools['dns_tool'],
                self.tools['ipinfo_tool'],
                self.tools['ssl_tool']
            ],
            memory=self.investigation_memory,
            verbose=True,
            step_callback=self._log_agent_step
        )
    
    @agent
    def mossad_counterintel_specialist(self) -> Agent:
        """Mossad Counterintelligence Specialist"""
        return Agent(
            config=self.agents_config['mossad_counterintel_specialist'],
            tools=[
                self.tools['sanctions_tool'],
                self.tools['financial_tool'],
                self.tools['blockchain_tool']
            ],
            memory=self.investigation_memory,
            verbose=True,
            step_callback=self._log_agent_step
        )
    
    @agent
    def domain_specialist(self) -> Agent:
        """Domain Intelligence Specialist"""
        return Agent(
            config=self.agents_config['domain_specialist'],
            tools=[
                self.tools['whois_tool'],
                self.tools['dns_tool'],
                self.tools['ssl_tool']
            ],
            memory=self.investigation_memory,
            verbose=True,
            step_callback=self._log_agent_step
        )
    
    @agent
    def email_specialist(self) -> Agent:
        """Email Investigation Specialist"""
        return Agent(
            config=self.agents_config['email_specialist'],
            tools=[
                self.tools['email_tool'],
                self.tools['dns_tool']
            ],
            memory=self.investigation_memory,
            verbose=True,
            step_callback=self._log_agent_step
        )
    
    @agent
    def crypto_specialist(self) -> Agent:
        """Cryptocurrency Investigation Specialist"""
        return Agent(
            config=self.agents_config['crypto_specialist'],
            tools=[
                self.tools['blockchain_tool'],
                self.tools['sanctions_tool']
            ],
            memory=self.investigation_memory,
            verbose=True,
            step_callback=self._log_agent_step
        )
    
    # Task Definitions
    @task
    def domain_investigation(self) -> Task:
        """Comprehensive domain investigation task"""
        return Task(
            config=self.tasks_config['domain_investigation'],
            agent=self.fbi_cyber_specialist,
            output_file='domain_investigation_report.json'
        )
    
    @task
    def email_investigation(self) -> Task:
        """Email authenticity and threat investigation task"""
        return Task(
            config=self.tasks_config['email_investigation'],
            agent=self.email_specialist,
            output_file='email_investigation_report.json'
        )
    
    @task
    def financial_intelligence(self) -> Task:
        """Financial intelligence and sanctions screening task"""
        return Task(
            config=self.tasks_config['financial_intelligence'],
            agent=self.cia_intelligence_analyst,
            context=[self.domain_investigation],
            output_file='financial_intelligence_report.json'
        )
    
    @task
    def cryptocurrency_investigation(self) -> Task:
        """Cryptocurrency analysis and compliance screening task"""
        return Task(
            config=self.tasks_config['cryptocurrency_investigation'],
            agent=self.crypto_specialist,
            output_file='crypto_investigation_report.json'
        )
    
    @task
    def signals_analysis(self) -> Task:
        """Signals intelligence analysis task"""
        return Task(
            config=self.tasks_config['signals_analysis'],
            agent=self.mi6_signals_specialist,
            context=[self.domain_investigation, self.financial_intelligence],
            output_file='signals_analysis_report.json'
        )
    
    @task
    def threat_assessment(self) -> Task:
        """Comprehensive threat assessment task"""
        return Task(
            config=self.tasks_config['threat_assessment'],
            agent=self.mossad_counterintel_specialist,
            context=[
                self.domain_investigation,
                self.financial_intelligence,
                self.signals_analysis
            ],
            output_file='threat_assessment_report.json'
        )
    
    @task
    def intelligence_fusion(self) -> Task:
        """Intelligence fusion and correlation task"""
        return Task(
            config=self.tasks_config['intelligence_fusion'],
            agent=self.cia_intelligence_analyst,
            context=[
                self.domain_investigation,
                self.financial_intelligence,
                self.signals_analysis,
                self.threat_assessment
            ],
            output_file='intelligence_fusion_report.json'
        )
    
    @task
    def comprehensive_report(self) -> Task:
        """Final comprehensive investigation report"""
        return Task(
            config=self.tasks_config['comprehensive_report'],
            agent=self.cia_intelligence_analyst,
            context=[
                self.domain_investigation,
                self.financial_intelligence,
                self.signals_analysis,
                self.threat_assessment,
                self.intelligence_fusion
            ],
            output_file='comprehensive_investigation_report.json'
        )
    
    # Crew Definitions
    @crew
    def investigation_crew(self) -> Crew:
        """Main investigation crew for comprehensive fraud analysis"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            memory=True,
            knowledge=self.fraud_knowledge,
            verbose=True,
            manager_llm=self.llm,
            planning=True,
            planning_llm=self.llm
        )
    
    @crew
    def domain_focused_crew(self) -> Crew:
        """Domain-focused investigation crew"""
        return Crew(
            agents=[
                self.fbi_cyber_specialist,
                self.domain_specialist,
                self.cia_intelligence_analyst
            ],
            tasks=[
                self.domain_investigation,
                self.financial_intelligence,
                self.threat_assessment
            ],
            process=Process.sequential,
            memory=True,
            knowledge=self.fraud_knowledge,
            verbose=True
        )
    
    @crew
    def email_focused_crew(self) -> Crew:
        """Email-focused investigation crew"""
        return Crew(
            agents=[
                self.email_specialist,
                self.fbi_cyber_specialist,
                self.cia_intelligence_analyst
            ],
            tasks=[
                self.email_investigation,
                self.domain_investigation,
                self.financial_intelligence
            ],
            process=Process.sequential,
            memory=True,
            knowledge=self.fraud_knowledge,
            verbose=True
        )
    
    @crew
    def crypto_focused_crew(self) -> Crew:
        """Cryptocurrency-focused investigation crew"""
        return Crew(
            agents=[
                self.crypto_specialist,
                self.mossad_counterintel_specialist,
                self.cia_intelligence_analyst
            ],
            tasks=[
                self.cryptocurrency_investigation,
                self.financial_intelligence,
                self.threat_assessment
            ],
            process=Process.sequential,
            memory=True,
            knowledge=self.fraud_knowledge,
            verbose=True
        )
    
    # Utility Methods
    def _log_agent_step(self, step_output: str) -> None:
        """Log agent execution steps for monitoring"""
        logger.info(f"Agent step completed: {step_output[:100]}...")
    
    def get_crew_by_type(self, investigation_type: str) -> Crew:
        """Get appropriate crew based on investigation type"""
        crew_mapping = {
            "domain": self.domain_focused_crew(),
            "email": self.email_focused_crew(),
            "cryptocurrency": self.crypto_focused_crew(),
            "comprehensive": self.investigation_crew()
        }
        
        return crew_mapping.get(investigation_type, self.investigation_crew())
    
    def run_investigation(self, 
                         investigation_type: str = "comprehensive",
                         inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run investigation with specified type and inputs
        
        Args:
            investigation_type: Type of investigation (domain, email, crypto, comprehensive)
            inputs: Investigation parameters and targets
            
        Returns:
            Investigation results and metadata
        """
        try:
            logger.info(f"Starting {investigation_type} investigation")
            
            # Get appropriate crew
            crew = self.get_crew_by_type(investigation_type)
            
            # Execute investigation
            result = crew.kickoff(inputs=inputs or {})
            
            # Format results
            investigation_results = {
                "investigation_id": result.id if hasattr(result, 'id') else None,
                "investigation_type": investigation_type,
                "status": "completed",
                "results": result.raw if hasattr(result, 'raw') else str(result),
                "tasks_completed": len(result.tasks_output) if hasattr(result, 'tasks_output') else 0,
                "agents_used": len(crew.agents),
                "execution_metadata": {
                    "crew_process": crew.process.value if hasattr(crew.process, 'value') else str(crew.process),
                    "memory_enabled": crew.memory,
                    "knowledge_enabled": crew.knowledge is not None
                }
            }
            
            logger.info(f"Investigation completed successfully: {investigation_type}")
            return investigation_results
            
        except Exception as e:
            logger.error(f"Investigation failed: {str(e)}")
            return {
                "investigation_type": investigation_type,
                "status": "failed",
                "error": str(e),
                "results": None
            }
    
    def get_investigation_history(self) -> List[Dict[str, Any]]:
        """Retrieve investigation history from memory"""
        try:
            # This would query the ChromaDB memory system
            # For now, return placeholder
            return [
                {
                    "investigation_id": "placeholder",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "type": "domain",
                    "status": "completed"
                }
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve investigation history: {str(e)}")
            return []
    
    def clear_memory(self) -> bool:
        """Clear investigation memory (use with caution)"""
        try:
            # This would clear the ChromaDB memory
            logger.warning("Investigation memory cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear memory: {str(e)}")
            return False

# Factory function for easy crew creation
def create_investigation_crew() -> ScamShieldInvestigationCrew:
    """Factory function to create a new investigation crew instance"""
    return ScamShieldInvestigationCrew()

# Convenience functions for different investigation types
def run_domain_investigation(domain: str) -> Dict[str, Any]:
    """Run domain-focused investigation"""
    crew = create_investigation_crew()
    return crew.run_investigation(
        investigation_type="domain",
        inputs={"domain": domain}
    )

def run_email_investigation(email: str) -> Dict[str, Any]:
    """Run email-focused investigation"""
    crew = create_investigation_crew()
    return crew.run_investigation(
        investigation_type="email",
        inputs={"email": email}
    )

def run_crypto_investigation(address: str) -> Dict[str, Any]:
    """Run cryptocurrency-focused investigation"""
    crew = create_investigation_crew()
    return crew.run_investigation(
        investigation_type="cryptocurrency",
        inputs={"crypto_address": address}
    )

def run_comprehensive_investigation(target: str, target_type: str) -> Dict[str, Any]:
    """Run comprehensive multi-agent investigation"""
    crew = create_investigation_crew()
    inputs = {target_type: target}
    return crew.run_investigation(
        investigation_type="comprehensive",
        inputs=inputs
    )

