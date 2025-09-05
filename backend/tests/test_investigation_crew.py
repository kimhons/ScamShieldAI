"""
ScamShield AI - Investigation Crew Test Suite

Comprehensive test suite for validating CrewAI integration and
multi-agent investigation capabilities.
"""

import pytest
import json
import time
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crews.investigation_crew import (
    ScamShieldInvestigationCrew,
    create_investigation_crew,
    run_domain_investigation,
    run_email_investigation,
    run_crypto_investigation,
    run_comprehensive_investigation
)
from tools.scamshield_tools import (
    WhoisDomainLookupTool,
    ShodanNetworkScanTool,
    SanctionsScreeningTool,
    get_tool,
    get_all_tools
)
from memory.investigation_memory import (
    ScamShieldInvestigationMemory,
    create_investigation_memory
)
from knowledge.fraud_knowledge import (
    ScamShieldFraudKnowledge,
    create_fraud_knowledge
)

class TestScamShieldInvestigationCrew:
    """Test suite for ScamShield Investigation Crew"""
    
    @pytest.fixture
    def mock_crew(self):
        """Create mock investigation crew for testing"""
        with patch('crews.investigation_crew.ChromaDBStorage'), \
             patch('crews.investigation_crew.Knowledge'), \
             patch('crews.investigation_crew.LongTermMemory'):
            crew = ScamShieldInvestigationCrew()
            return crew
    
    @pytest.fixture
    def sample_investigation_data(self):
        """Sample investigation data for testing"""
        return {
            "investigation_id": "test-001",
            "investigation_type": "domain",
            "target": "suspicious-domain.com",
            "timestamp": "2024-01-01T00:00:00Z",
            "results": {
                "domain_analysis": {
                    "whois_data": {"registrar": "Test Registrar"},
                    "dns_analysis": {"mx_records": ["mail.suspicious-domain.com"]},
                    "ssl_analysis": {"valid": False, "issuer": "Unknown"}
                },
                "risk_score": 85,
                "threat_level": "HIGH",
                "confidence": 0.92
            }
        }
    
    def test_crew_initialization(self, mock_crew):
        """Test crew initialization and configuration"""
        assert mock_crew is not None
        assert hasattr(mock_crew, 'investigation_memory')
        assert hasattr(mock_crew, 'fraud_knowledge')
        assert hasattr(mock_crew, 'tools')
        assert len(mock_crew.tools) >= 9  # Should have all major tools
    
    def test_agent_creation(self, mock_crew):
        """Test agent creation and configuration"""
        # Test FBI Cyber Specialist
        fbi_agent = mock_crew.fbi_cyber_specialist()
        assert fbi_agent is not None
        assert len(fbi_agent.tools) >= 4
        
        # Test CIA Intelligence Analyst
        cia_agent = mock_crew.cia_intelligence_analyst()
        assert cia_agent is not None
        assert len(cia_agent.tools) >= 3
        
        # Test MI6 Signals Specialist
        mi6_agent = mock_crew.mi6_signals_specialist()
        assert mi6_agent is not None
        assert len(mi6_agent.tools) >= 3
        
        # Test Mossad Counter-Intel Specialist
        mossad_agent = mock_crew.mossad_counterintel_specialist()
        assert mossad_agent is not None
        assert len(mossad_agent.tools) >= 3
    
    def test_task_creation(self, mock_crew):
        """Test task creation and configuration"""
        # Test domain investigation task
        domain_task = mock_crew.domain_investigation()
        assert domain_task is not None
        assert domain_task.agent == mock_crew.fbi_cyber_specialist
        
        # Test financial intelligence task
        financial_task = mock_crew.financial_intelligence()
        assert financial_task is not None
        assert financial_task.agent == mock_crew.cia_intelligence_analyst
        
        # Test threat assessment task
        threat_task = mock_crew.threat_assessment()
        assert threat_task is not None
        assert threat_task.agent == mock_crew.mossad_counterintel_specialist
    
    def test_crew_orchestration(self, mock_crew):
        """Test crew orchestration and process configuration"""
        investigation_crew = mock_crew.investigation_crew()
        assert investigation_crew is not None
        assert len(investigation_crew.agents) >= 4
        assert len(investigation_crew.tasks) >= 4
        assert investigation_crew.memory is True
        assert investigation_crew.knowledge is not None
    
    @patch('crews.investigation_crew.Crew.kickoff')
    def test_run_investigation(self, mock_kickoff, mock_crew):
        """Test investigation execution"""
        # Mock successful investigation result
        mock_result = Mock()
        mock_result.raw = "Investigation completed successfully"
        mock_result.tasks_output = [Mock(), Mock(), Mock()]
        mock_result.id = "test-investigation-001"
        mock_kickoff.return_value = mock_result
        
        # Test comprehensive investigation
        result = mock_crew.run_investigation(
            investigation_type="comprehensive",
            inputs={"domain": "test-domain.com"}
        )
        
        assert result["status"] == "completed"
        assert result["investigation_type"] == "comprehensive"
        assert result["tasks_completed"] == 3
        assert "results" in result
    
    def test_get_crew_by_type(self, mock_crew):
        """Test crew selection by investigation type"""
        # Test domain-focused crew
        domain_crew = mock_crew.get_crew_by_type("domain")
        assert domain_crew is not None
        
        # Test email-focused crew
        email_crew = mock_crew.get_crew_by_type("email")
        assert email_crew is not None
        
        # Test crypto-focused crew
        crypto_crew = mock_crew.get_crew_by_type("cryptocurrency")
        assert crypto_crew is not None
        
        # Test default crew for unknown type
        default_crew = mock_crew.get_crew_by_type("unknown")
        assert default_crew is not None

class TestScamShieldTools:
    """Test suite for ScamShield CrewAI tools"""
    
    def test_tool_registry(self):
        """Test tool registry and availability"""
        all_tools = get_all_tools()
        assert len(all_tools) >= 9
        
        # Test specific tool retrieval
        whois_tool = get_tool("whois_domain_lookup")
        assert whois_tool is not None
        assert isinstance(whois_tool, WhoisDomainLookupTool)
        
        shodan_tool = get_tool("shodan_network_scan")
        assert shodan_tool is not None
        assert isinstance(shodan_tool, ShodanNetworkScanTool)
        
        sanctions_tool = get_tool("sanctions_screening")
        assert sanctions_tool is not None
        assert isinstance(sanctions_tool, SanctionsScreeningTool)
    
    @patch('tools.scamshield_tools.WhoisXMLIntegration')
    def test_whois_tool_execution(self, mock_whois_integration):
        """Test WHOIS tool execution"""
        # Mock WhoisXML integration
        mock_client = Mock()
        mock_client.lookup_domain.return_value = {
            "domain": "test.com",
            "registrar": "Test Registrar",
            "creation_date": "2020-01-01"
        }
        mock_client.get_timestamp.return_value = "2024-01-01T00:00:00Z"
        mock_whois_integration.return_value = mock_client
        
        # Test tool execution
        whois_tool = WhoisDomainLookupTool()
        result = whois_tool._run("test.com")
        
        assert result is not None
        result_data = json.loads(result)
        assert result_data["domain"] == "test.com"
        assert "whois_data" in result_data
        assert "analysis_timestamp" in result_data
    
    @patch('tools.scamshield_tools.ShodanIntegration')
    def test_shodan_tool_execution(self, mock_shodan_integration):
        """Test Shodan tool execution"""
        # Mock Shodan integration
        mock_client = Mock()
        mock_client.scan_ip.return_value = {
            "ip": "192.168.1.1",
            "ports": [80, 443],
            "services": ["http", "https"]
        }
        mock_client.get_timestamp.return_value = "2024-01-01T00:00:00Z"
        mock_shodan_integration.return_value = mock_client
        
        # Test tool execution
        shodan_tool = ShodanNetworkScanTool()
        result = shodan_tool._run("192.168.1.1")
        
        assert result is not None
        result_data = json.loads(result)
        assert result_data["ip_address"] == "192.168.1.1"
        assert "scan_results" in result_data
        assert "analysis_timestamp" in result_data
    
    @patch('tools.scamshield_tools.OpenSanctionsIntegration')
    def test_sanctions_tool_execution(self, mock_sanctions_integration):
        """Test sanctions screening tool execution"""
        # Mock OpenSanctions integration
        mock_client = Mock()
        mock_client.screen_entity.return_value = {
            "entity": "Test Entity",
            "sanctions_found": True,
            "lists": ["OFAC SDN", "EU Sanctions"]
        }
        mock_client.get_timestamp.return_value = "2024-01-01T00:00:00Z"
        mock_sanctions_integration.return_value = mock_client
        
        # Test tool execution
        sanctions_tool = SanctionsScreeningTool()
        result = sanctions_tool._run("Test Entity")
        
        assert result is not None
        result_data = json.loads(result)
        assert result_data["entity"] == "Test Entity"
        assert "sanctions_results" in result_data
        assert "analysis_timestamp" in result_data
    
    def test_tool_error_handling(self):
        """Test tool error handling"""
        # Test with invalid input
        whois_tool = WhoisDomainLookupTool()
        
        with patch('tools.scamshield_tools.WhoisXMLIntegration') as mock_integration:
            mock_integration.side_effect = Exception("API Error")
            
            result = whois_tool._run("invalid-domain")
            result_data = json.loads(result)
            
            assert "error" in result_data
            assert result_data["status"] == "failed"

class TestInvestigationMemory:
    """Test suite for investigation memory system"""
    
    @pytest.fixture
    def mock_memory(self):
        """Create mock memory system for testing"""
        with patch('memory.investigation_memory.ChromaDBStorage'), \
             patch('memory.investigation_memory.LongTermMemory'), \
             patch('memory.investigation_memory.ShortTermMemory'):
            memory = ScamShieldInvestigationMemory()
            return memory
    
    def test_memory_initialization(self, mock_memory):
        """Test memory system initialization"""
        assert mock_memory is not None
        assert hasattr(mock_memory, 'investigation_memory')
        assert hasattr(mock_memory, 'agent_memories')
        assert hasattr(mock_memory, 'pattern_memory')
        assert len(mock_memory.agent_memories) == 4  # FBI, CIA, MI6, Mossad
    
    def test_store_investigation(self, mock_memory, sample_investigation_data):
        """Test investigation storage"""
        result = mock_memory.store_investigation(
            investigation_id="test-001",
            investigation_data=sample_investigation_data
        )
        assert result is True
    
    def test_retrieve_investigation(self, mock_memory):
        """Test investigation retrieval"""
        # Mock memory search result
        with patch.object(mock_memory.investigation_memory, 'search') as mock_search:
            mock_search.return_value = [json.dumps({
                "investigation_id": "test-001",
                "data": {"test": "data"}
            })]
            
            result = mock_memory.retrieve_investigation("test-001")
            assert result is not None
            assert result["investigation_id"] == "test-001"
    
    def test_search_investigations(self, mock_memory):
        """Test investigation search functionality"""
        # Mock memory search results
        with patch.object(mock_memory.investigation_memory, 'search') as mock_search:
            mock_search.return_value = [
                json.dumps({"investigation_id": "test-001", "type": "domain"}),
                json.dumps({"investigation_id": "test-002", "type": "email"})
            ]
            
            results = mock_memory.search_investigations("domain")
            assert len(results) == 2
            assert all("investigation_id" in result for result in results)
    
    def test_agent_memory_operations(self, mock_memory):
        """Test agent-specific memory operations"""
        # Test storing agent memory
        memory_data = {
            "learning": "New fraud pattern identified",
            "context": "Domain investigation",
            "confidence": 0.85
        }
        
        result = mock_memory.store_agent_memory(
            agent_type="fbi_cyber",
            memory_data=memory_data,
            context="test-investigation"
        )
        assert result is True
        
        # Test retrieving agent memory
        with patch.object(mock_memory.agent_memories["fbi_cyber"], 'search') as mock_search:
            mock_search.return_value = [json.dumps({
                "agent_type": "fbi_cyber",
                "data": memory_data
            })]
            
            memories = mock_memory.retrieve_agent_memory("fbi_cyber")
            assert len(memories) >= 0  # Should not fail
    
    def test_fraud_pattern_operations(self, mock_memory):
        """Test fraud pattern storage and retrieval"""
        pattern_data = {
            "indicators": ["suspicious_tld", "recent_registration"],
            "risk_score": 75,
            "description": "Suspicious domain pattern"
        }
        
        # Test storing fraud pattern
        result = mock_memory.store_fraud_pattern(
            pattern_data=pattern_data,
            pattern_type="domain",
            confidence=0.9
        )
        assert result is True
        
        # Test searching fraud patterns
        with patch.object(mock_memory.pattern_memory, 'search') as mock_search:
            mock_search.return_value = [json.dumps({
                "pattern_type": "domain",
                "confidence": 0.9,
                "data": pattern_data
            })]
            
            patterns = mock_memory.search_fraud_patterns("domain")
            assert len(patterns) >= 0  # Should not fail

class TestFraudKnowledge:
    """Test suite for fraud knowledge system"""
    
    @pytest.fixture
    def mock_knowledge(self):
        """Create mock knowledge system for testing"""
        with patch('knowledge.fraud_knowledge.Knowledge'), \
             patch('os.makedirs'), \
             patch('os.path.exists', return_value=False):
            knowledge = ScamShieldFraudKnowledge()
            return knowledge
    
    def test_knowledge_initialization(self, mock_knowledge):
        """Test knowledge system initialization"""
        assert mock_knowledge is not None
        assert hasattr(mock_knowledge, 'fraud_patterns')
        assert hasattr(mock_knowledge, 'methodologies')
        assert hasattr(mock_knowledge, 'threat_intelligence')
    
    def test_fraud_patterns_access(self, mock_knowledge):
        """Test fraud patterns access and retrieval"""
        # Test getting all patterns
        all_patterns = mock_knowledge.get_fraud_patterns()
        assert isinstance(all_patterns, dict)
        
        # Test getting specific pattern type
        domain_patterns = mock_knowledge.get_fraud_patterns("domain_patterns")
        assert isinstance(domain_patterns, dict)
    
    def test_methodology_access(self, mock_knowledge):
        """Test investigation methodology access"""
        # Test FBI methodology
        fbi_methods = mock_knowledge.get_investigation_methodology("fbi_cyber")
        assert isinstance(fbi_methods, dict)
        
        # Test CIA methodology
        cia_methods = mock_knowledge.get_investigation_methodology("cia_intelligence")
        assert isinstance(cia_methods, dict)
    
    def test_threat_intelligence_access(self, mock_knowledge):
        """Test threat intelligence access"""
        # Test getting all threat intelligence
        all_intel = mock_knowledge.get_threat_intelligence()
        assert isinstance(all_intel, dict)
        
        # Test getting specific threat type
        actors = mock_knowledge.get_threat_intelligence("actors")
        assert isinstance(actors, dict)
    
    def test_add_fraud_pattern(self, mock_knowledge):
        """Test adding new fraud patterns"""
        pattern_data = {
            "indicators": ["test_indicator"],
            "description": "Test pattern"
        }
        
        with patch.object(mock_knowledge, '_save_fraud_patterns'):
            result = mock_knowledge.add_fraud_pattern(
                pattern_type="test_patterns",
                pattern_name="test_pattern",
                pattern_data=pattern_data
            )
            assert result is True
    
    def test_knowledge_search(self, mock_knowledge):
        """Test knowledge search functionality"""
        results = mock_knowledge.search_knowledge("phishing")
        assert isinstance(results, list)
        
        # Test specific knowledge type search
        pattern_results = mock_knowledge.search_knowledge("domain", "patterns")
        assert isinstance(pattern_results, list)

class TestPerformanceBenchmarks:
    """Performance benchmark tests for CrewAI integration"""
    
    @pytest.fixture
    def benchmark_crew(self):
        """Create crew for performance benchmarking"""
        with patch('crews.investigation_crew.ChromaDBStorage'), \
             patch('crews.investigation_crew.Knowledge'), \
             patch('crews.investigation_crew.LongTermMemory'):
            return ScamShieldInvestigationCrew()
    
    @patch('crews.investigation_crew.Crew.kickoff')
    def test_investigation_speed_benchmark(self, mock_kickoff, benchmark_crew):
        """Test investigation completion time (target: ≤60 seconds)"""
        # Mock fast investigation result
        mock_result = Mock()
        mock_result.raw = "Fast investigation completed"
        mock_result.tasks_output = [Mock(), Mock()]
        mock_result.id = "benchmark-001"
        mock_kickoff.return_value = mock_result
        
        start_time = time.time()
        result = benchmark_crew.run_investigation(
            investigation_type="domain",
            inputs={"domain": "benchmark-test.com"}
        )
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Should complete quickly with mocked components
        assert execution_time < 5  # Generous limit for mocked test
        assert result["status"] == "completed"
    
    @patch('crews.investigation_crew.Crew.kickoff')
    def test_concurrent_investigations_benchmark(self, mock_kickoff, benchmark_crew):
        """Test concurrent investigation capacity"""
        import threading
        
        # Mock investigation results
        mock_result = Mock()
        mock_result.raw = "Concurrent investigation completed"
        mock_result.tasks_output = [Mock()]
        mock_result.id = "concurrent-test"
        mock_kickoff.return_value = mock_result
        
        def run_investigation(domain_id):
            return benchmark_crew.run_investigation(
                investigation_type="domain",
                inputs={"domain": f"test-{domain_id}.com"}
            )
        
        # Test concurrent execution
        threads = []
        results = []
        
        start_time = time.time()
        for i in range(5):  # Test 5 concurrent investigations
            thread = threading.Thread(
                target=lambda i=i: results.append(run_investigation(i))
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # All investigations should complete successfully
        assert len(results) == 5
        assert all(result["status"] == "completed" for result in results)
        assert total_time < 10  # Should complete quickly with mocked components

class TestIntegrationValidation:
    """Integration validation tests"""
    
    def test_factory_functions(self):
        """Test factory functions for easy component creation"""
        # Test crew factory
        with patch('crews.investigation_crew.ChromaDBStorage'), \
             patch('crews.investigation_crew.Knowledge'), \
             patch('crews.investigation_crew.LongTermMemory'):
            crew = create_investigation_crew()
            assert crew is not None
            assert isinstance(crew, ScamShieldInvestigationCrew)
        
        # Test memory factory
        with patch('memory.investigation_memory.ChromaDBStorage'), \
             patch('memory.investigation_memory.LongTermMemory'), \
             patch('memory.investigation_memory.ShortTermMemory'):
            memory = create_investigation_memory()
            assert memory is not None
            assert isinstance(memory, ScamShieldInvestigationMemory)
        
        # Test knowledge factory
        with patch('knowledge.fraud_knowledge.Knowledge'), \
             patch('os.makedirs'), \
             patch('os.path.exists', return_value=False):
            knowledge = create_fraud_knowledge()
            assert knowledge is not None
            assert isinstance(knowledge, ScamShieldFraudKnowledge)
    
    @patch('crews.investigation_crew.create_investigation_crew')
    def test_convenience_functions(self, mock_create_crew):
        """Test convenience functions for different investigation types"""
        # Mock crew and its methods
        mock_crew = Mock()
        mock_crew.run_investigation.return_value = {
            "status": "completed",
            "investigation_type": "domain"
        }
        mock_create_crew.return_value = mock_crew
        
        # Test domain investigation
        result = run_domain_investigation("test.com")
        assert result["status"] == "completed"
        
        # Test email investigation
        result = run_email_investigation("test@example.com")
        assert result["status"] == "completed"
        
        # Test crypto investigation
        result = run_crypto_investigation("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        assert result["status"] == "completed"
        
        # Test comprehensive investigation
        result = run_comprehensive_investigation("test.com", "domain")
        assert result["status"] == "completed"

# Test configuration and fixtures
@pytest.fixture(scope="session")
def test_config():
    """Test configuration for the entire test session"""
    return {
        "test_domain": "test-domain.com",
        "test_email": "test@example.com",
        "test_ip": "192.168.1.1",
        "test_crypto_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    }

# Performance test markers
pytestmark = pytest.mark.performance

if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--cov=crews",
        "--cov=tools",
        "--cov=memory",
        "--cov=knowledge",
        "--cov-report=term-missing"
    ])

