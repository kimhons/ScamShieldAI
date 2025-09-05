"""
ScamShield AI - Investigation Memory Management

This module implements the memory management system for ScamShield investigations
using ChromaDB for persistent storage and retrieval of investigation data.
"""

from crewai.memory import LongTermMemory, ShortTermMemory
from crewai.memory.storage import ChromaDBStorage
from typing import Dict, List, Any, Optional
import json
import logging
from datetime import datetime, timedelta
import uuid

# Configure logging
logger = logging.getLogger(__name__)

class ScamShieldInvestigationMemory:
    """
    Comprehensive memory management system for ScamShield investigations
    with persistent storage, retrieval, and analysis capabilities.
    """
    
    def __init__(self, persist_directory: str = "./memory"):
        """
        Initialize the investigation memory system
        
        Args:
            persist_directory: Directory for persistent memory storage
        """
        self.persist_directory = persist_directory
        
        # Initialize long-term memory for investigations
        self.investigation_memory = LongTermMemory(
            storage=ChromaDBStorage(
                collection_name="scamshield_investigations",
                persist_directory=f"{persist_directory}/investigations"
            )
        )
        
        # Initialize agent-specific memories
        self.agent_memories = {
            "fbi_cyber": LongTermMemory(
                storage=ChromaDBStorage(
                    collection_name="fbi_cyber_memory",
                    persist_directory=f"{persist_directory}/agents/fbi_cyber"
                )
            ),
            "cia_intelligence": LongTermMemory(
                storage=ChromaDBStorage(
                    collection_name="cia_intelligence_memory",
                    persist_directory=f"{persist_directory}/agents/cia_intelligence"
                )
            ),
            "mi6_signals": LongTermMemory(
                storage=ChromaDBStorage(
                    collection_name="mi6_signals_memory",
                    persist_directory=f"{persist_directory}/agents/mi6_signals"
                )
            ),
            "mossad_counterintel": LongTermMemory(
                storage=ChromaDBStorage(
                    collection_name="mossad_counterintel_memory",
                    persist_directory=f"{persist_directory}/agents/mossad_counterintel"
                )
            )
        }
        
        # Initialize pattern memory for fraud detection
        self.pattern_memory = LongTermMemory(
            storage=ChromaDBStorage(
                collection_name="fraud_patterns",
                persist_directory=f"{persist_directory}/patterns"
            )
        )
        
        # Initialize short-term memory for active investigations
        self.active_memory = ShortTermMemory()
        
        logger.info("ScamShield Investigation Memory initialized")
    
    def store_investigation(self, 
                          investigation_id: str,
                          investigation_data: Dict[str, Any],
                          metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Store investigation results in long-term memory
        
        Args:
            investigation_id: Unique investigation identifier
            investigation_data: Complete investigation results
            metadata: Additional metadata about the investigation
            
        Returns:
            Success status of storage operation
        """
        try:
            # Prepare investigation record
            investigation_record = {
                "investigation_id": investigation_id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": investigation_data,
                "metadata": metadata or {},
                "status": "completed"
            }
            
            # Store in investigation memory
            self.investigation_memory.save(
                value=json.dumps(investigation_record),
                metadata={
                    "investigation_id": investigation_id,
                    "timestamp": investigation_record["timestamp"],
                    "type": investigation_data.get("investigation_type", "unknown")
                }
            )
            
            logger.info(f"Investigation {investigation_id} stored in memory")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store investigation {investigation_id}: {str(e)}")
            return False
    
    def retrieve_investigation(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve specific investigation from memory
        
        Args:
            investigation_id: Investigation identifier to retrieve
            
        Returns:
            Investigation data if found, None otherwise
        """
        try:
            # Search for investigation by ID
            results = self.investigation_memory.search(
                query=f"investigation_id:{investigation_id}",
                limit=1
            )
            
            if results:
                investigation_data = json.loads(results[0])
                logger.info(f"Retrieved investigation {investigation_id}")
                return investigation_data
            
            logger.warning(f"Investigation {investigation_id} not found")
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve investigation {investigation_id}: {str(e)}")
            return None
    
    def search_investigations(self, 
                            query: str,
                            limit: int = 10,
                            filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search investigations based on query and filters
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            filters: Additional filters for search
            
        Returns:
            List of matching investigations
        """
        try:
            # Perform search in investigation memory
            results = self.investigation_memory.search(
                query=query,
                limit=limit
            )
            
            investigations = []
            for result in results:
                try:
                    investigation = json.loads(result)
                    
                    # Apply filters if provided
                    if filters:
                        if self._matches_filters(investigation, filters):
                            investigations.append(investigation)
                    else:
                        investigations.append(investigation)
                        
                except json.JSONDecodeError:
                    logger.warning("Failed to parse investigation result")
                    continue
            
            logger.info(f"Found {len(investigations)} investigations matching query: {query}")
            return investigations
            
        except Exception as e:
            logger.error(f"Failed to search investigations: {str(e)}")
            return []
    
    def store_agent_memory(self, 
                          agent_type: str,
                          memory_data: Dict[str, Any],
                          context: Optional[str] = None) -> bool:
        """
        Store agent-specific memory and learning
        
        Args:
            agent_type: Type of agent (fbi_cyber, cia_intelligence, etc.)
            memory_data: Agent memory data to store
            context: Context or investigation ID for the memory
            
        Returns:
            Success status of storage operation
        """
        try:
            if agent_type not in self.agent_memories:
                logger.error(f"Unknown agent type: {agent_type}")
                return False
            
            # Prepare memory record
            memory_record = {
                "agent_type": agent_type,
                "timestamp": datetime.utcnow().isoformat(),
                "context": context,
                "data": memory_data,
                "memory_id": str(uuid.uuid4())
            }
            
            # Store in agent-specific memory
            self.agent_memories[agent_type].save(
                value=json.dumps(memory_record),
                metadata={
                    "agent_type": agent_type,
                    "timestamp": memory_record["timestamp"],
                    "context": context or "general"
                }
            )
            
            logger.info(f"Stored memory for agent {agent_type}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store agent memory for {agent_type}: {str(e)}")
            return False
    
    def retrieve_agent_memory(self, 
                            agent_type: str,
                            context: Optional[str] = None,
                            limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve agent-specific memories
        
        Args:
            agent_type: Type of agent to retrieve memories for
            context: Specific context to filter memories
            limit: Maximum number of memories to retrieve
            
        Returns:
            List of agent memories
        """
        try:
            if agent_type not in self.agent_memories:
                logger.error(f"Unknown agent type: {agent_type}")
                return []
            
            # Build search query
            query = f"agent_type:{agent_type}"
            if context:
                query += f" context:{context}"
            
            # Search agent memory
            results = self.agent_memories[agent_type].search(
                query=query,
                limit=limit
            )
            
            memories = []
            for result in results:
                try:
                    memory = json.loads(result)
                    memories.append(memory)
                except json.JSONDecodeError:
                    logger.warning("Failed to parse agent memory result")
                    continue
            
            logger.info(f"Retrieved {len(memories)} memories for agent {agent_type}")
            return memories
            
        except Exception as e:
            logger.error(f"Failed to retrieve agent memory for {agent_type}: {str(e)}")
            return []
    
    def store_fraud_pattern(self, 
                           pattern_data: Dict[str, Any],
                           pattern_type: str,
                           confidence: float = 1.0) -> bool:
        """
        Store identified fraud patterns for future detection
        
        Args:
            pattern_data: Fraud pattern data and indicators
            pattern_type: Type of fraud pattern (domain, email, financial, etc.)
            confidence: Confidence level of the pattern (0.0 to 1.0)
            
        Returns:
            Success status of storage operation
        """
        try:
            # Prepare pattern record
            pattern_record = {
                "pattern_id": str(uuid.uuid4()),
                "pattern_type": pattern_type,
                "timestamp": datetime.utcnow().isoformat(),
                "confidence": confidence,
                "data": pattern_data,
                "usage_count": 0
            }
            
            # Store in pattern memory
            self.pattern_memory.save(
                value=json.dumps(pattern_record),
                metadata={
                    "pattern_type": pattern_type,
                    "confidence": confidence,
                    "timestamp": pattern_record["timestamp"]
                }
            )
            
            logger.info(f"Stored fraud pattern: {pattern_type} (confidence: {confidence})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store fraud pattern: {str(e)}")
            return False
    
    def search_fraud_patterns(self, 
                            pattern_type: Optional[str] = None,
                            min_confidence: float = 0.5,
                            limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for fraud patterns matching criteria
        
        Args:
            pattern_type: Specific pattern type to search for
            min_confidence: Minimum confidence threshold
            limit: Maximum number of patterns to return
            
        Returns:
            List of matching fraud patterns
        """
        try:
            # Build search query
            query = f"confidence:>={min_confidence}"
            if pattern_type:
                query += f" pattern_type:{pattern_type}"
            
            # Search pattern memory
            results = self.pattern_memory.search(
                query=query,
                limit=limit
            )
            
            patterns = []
            for result in results:
                try:
                    pattern = json.loads(result)
                    if pattern.get("confidence", 0) >= min_confidence:
                        patterns.append(pattern)
                except json.JSONDecodeError:
                    logger.warning("Failed to parse fraud pattern result")
                    continue
            
            logger.info(f"Found {len(patterns)} fraud patterns matching criteria")
            return patterns
            
        except Exception as e:
            logger.error(f"Failed to search fraud patterns: {str(e)}")
            return []
    
    def get_investigation_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about stored investigations
        
        Returns:
            Dictionary containing investigation statistics
        """
        try:
            # Get recent investigations (last 30 days)
            recent_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
            recent_investigations = self.search_investigations(
                query=f"timestamp:>={recent_date}",
                limit=1000
            )
            
            # Calculate statistics
            stats = {
                "total_investigations": len(recent_investigations),
                "investigation_types": {},
                "success_rate": 0,
                "average_completion_time": 0,
                "most_common_threats": [],
                "memory_usage": {
                    "investigations": len(recent_investigations),
                    "patterns": len(self.search_fraud_patterns(limit=1000)),
                    "agent_memories": sum(
                        len(self.retrieve_agent_memory(agent_type, limit=1000))
                        for agent_type in self.agent_memories.keys()
                    )
                }
            }
            
            # Analyze investigation types
            for investigation in recent_investigations:
                inv_type = investigation.get("data", {}).get("investigation_type", "unknown")
                stats["investigation_types"][inv_type] = stats["investigation_types"].get(inv_type, 0) + 1
            
            # Calculate success rate
            successful = sum(1 for inv in recent_investigations if inv.get("status") == "completed")
            stats["success_rate"] = (successful / len(recent_investigations)) * 100 if recent_investigations else 0
            
            logger.info("Generated investigation statistics")
            return stats
            
        except Exception as e:
            logger.error(f"Failed to generate statistics: {str(e)}")
            return {"error": str(e)}
    
    def cleanup_old_memories(self, days_to_keep: int = 90) -> bool:
        """
        Clean up old memories to manage storage space
        
        Args:
            days_to_keep: Number of days of memories to retain
            
        Returns:
            Success status of cleanup operation
        """
        try:
            cutoff_date = (datetime.utcnow() - timedelta(days=days_to_keep)).isoformat()
            
            # This would implement cleanup logic for ChromaDB
            # For now, just log the operation
            logger.info(f"Memory cleanup initiated for data older than {cutoff_date}")
            
            # In a real implementation, this would:
            # 1. Query for old records
            # 2. Delete records older than cutoff_date
            # 3. Compact the database
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to cleanup old memories: {str(e)}")
            return False
    
    def _matches_filters(self, investigation: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """
        Check if investigation matches provided filters
        
        Args:
            investigation: Investigation data to check
            filters: Filters to apply
            
        Returns:
            True if investigation matches all filters
        """
        try:
            for key, value in filters.items():
                if key in investigation:
                    if investigation[key] != value:
                        return False
                elif key in investigation.get("data", {}):
                    if investigation["data"][key] != value:
                        return False
                elif key in investigation.get("metadata", {}):
                    if investigation["metadata"][key] != value:
                        return False
                else:
                    return False
            
            return True
            
        except Exception:
            return False

# Factory function for easy memory system creation
def create_investigation_memory(persist_directory: str = "./memory") -> ScamShieldInvestigationMemory:
    """
    Factory function to create investigation memory system
    
    Args:
        persist_directory: Directory for persistent storage
        
    Returns:
        Configured investigation memory system
    """
    return ScamShieldInvestigationMemory(persist_directory)

# Global memory instance (singleton pattern)
_global_memory_instance = None

def get_global_memory() -> ScamShieldInvestigationMemory:
    """
    Get global memory instance (singleton)
    
    Returns:
        Global investigation memory system
    """
    global _global_memory_instance
    if _global_memory_instance is None:
        _global_memory_instance = create_investigation_memory()
    return _global_memory_instance

