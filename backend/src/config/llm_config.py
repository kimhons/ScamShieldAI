"""
ScamShield AI - LLM Configuration for CrewAI

This module configures different LLM providers for CrewAI agents,
providing fallback options and load balancing across providers.
"""

import os
from typing import Dict, Any, Optional
from crewai import LLM
import logging

logger = logging.getLogger(__name__)

class LLMConfig:
    """Configuration manager for LLM providers"""
    
    def __init__(self):
        """Initialize LLM configuration with environment variables"""
        self.providers = {
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'model': os.getenv('OPENAI_MODEL', 'gpt-4'),
                'base_url': os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1'),
                'enabled': bool(os.getenv('OPENAI_API_KEY'))
            },
            'anthropic': {
                'api_key': os.getenv('ANTHROPIC_API_KEY'),
                'model': os.getenv('ANTHROPIC_MODEL', 'claude-3-opus-20240229'),
                'base_url': os.getenv('ANTHROPIC_ENDPOINT', 'https://api.anthropic.com/v1'),
                'enabled': bool(os.getenv('ANTHROPIC_API_KEY'))
            },
            'google': {
                'api_key': os.getenv('GOOGLE_API_KEY'),
                'model': os.getenv('GOOGLE_MODEL', 'gemini-pro'),
                'base_url': os.getenv('GOOGLE_ENDPOINT', 'https://generativelanguage.googleapis.com/v1beta'),
                'enabled': bool(os.getenv('GOOGLE_API_KEY'))
            },
            'deepseek': {
                'api_key': os.getenv('DEEPSEEK_API_KEY'),
                'model': os.getenv('DEEPSEEK_MODEL', 'deepseek-coder'),
                'base_url': os.getenv('DEEPSEEK_ENDPOINT', 'https://api.deepseek.com/v1'),
                'enabled': bool(os.getenv('DEEPSEEK_API_KEY'))
            }
        }
        
        # Log available providers
        enabled_providers = [name for name, config in self.providers.items() if config['enabled']]
        logger.info(f"Available LLM providers: {enabled_providers}")
    
    def get_primary_llm(self) -> LLM:
        """Get primary LLM (OpenAI GPT-4) for main agent operations"""
        if self.providers['openai']['enabled']:
            return LLM(
                model=f"openai/{self.providers['openai']['model']}",
                api_key=self.providers['openai']['api_key'],
                base_url=self.providers['openai']['base_url'],
                temperature=0.1,
                max_tokens=4000
            )
        else:
            return self._get_fallback_llm()
    
    def get_analysis_llm(self) -> LLM:
        """Get LLM optimized for analysis tasks (Claude)"""
        if self.providers['anthropic']['enabled']:
            return LLM(
                model=f"anthropic/{self.providers['anthropic']['model']}",
                api_key=self.providers['anthropic']['api_key'],
                base_url=self.providers['anthropic']['base_url'],
                temperature=0.0,
                max_tokens=4000
            )
        else:
            return self.get_primary_llm()
    
    def get_coding_llm(self) -> LLM:
        """Get LLM optimized for coding tasks (DeepSeek)"""
        if self.providers['deepseek']['enabled']:
            return LLM(
                model=f"openai/{self.providers['deepseek']['model']}",  # DeepSeek uses OpenAI-compatible API
                api_key=self.providers['deepseek']['api_key'],
                base_url=self.providers['deepseek']['base_url'],
                temperature=0.0,
                max_tokens=4000
            )
        else:
            return self.get_primary_llm()
    
    def get_creative_llm(self) -> LLM:
        """Get LLM optimized for creative tasks (Gemini)"""
        if self.providers['google']['enabled']:
            return LLM(
                model=f"google/{self.providers['google']['model']}",
                api_key=self.providers['google']['api_key'],
                base_url=self.providers['google']['base_url'],
                temperature=0.3,
                max_tokens=4000
            )
        else:
            return self.get_primary_llm()
    
    def _get_fallback_llm(self) -> LLM:
        """Get fallback LLM when primary is unavailable"""
        # Try providers in order of preference
        fallback_order = ['anthropic', 'google', 'deepseek']
        
        for provider in fallback_order:
            if self.providers[provider]['enabled']:
                config = self.providers[provider]
                logger.warning(f"Using fallback LLM: {provider}")
                
                if provider == 'anthropic':
                    return LLM(
                        model=f"anthropic/{config['model']}",
                        api_key=config['api_key'],
                        base_url=config['base_url'],
                        temperature=0.1,
                        max_tokens=4000
                    )
                elif provider == 'google':
                    return LLM(
                        model=f"google/{config['model']}",
                        api_key=config['api_key'],
                        base_url=config['base_url'],
                        temperature=0.1,
                        max_tokens=4000
                    )
                elif provider == 'deepseek':
                    return LLM(
                        model=f"openai/{config['model']}",
                        api_key=config['api_key'],
                        base_url=config['base_url'],
                        temperature=0.1,
                        max_tokens=4000
                    )
        
        raise RuntimeError("No LLM providers available! Please configure at least one API key.")
    
    def get_agent_llm(self, agent_type: str) -> LLM:
        """Get optimized LLM for specific agent type"""
        agent_llm_mapping = {
            'fbi_cyber_specialist': self.get_analysis_llm(),
            'cia_intelligence_analyst': self.get_analysis_llm(),
            'mi6_signals_specialist': self.get_analysis_llm(),
            'mossad_counterintel_specialist': self.get_analysis_llm(),
            'domain_specialist': self.get_primary_llm(),
            'email_specialist': self.get_primary_llm(),
            'financial_analyst': self.get_analysis_llm(),
            'crypto_specialist': self.get_coding_llm()
        }
        
        return agent_llm_mapping.get(agent_type, self.get_primary_llm())
    
    def get_crew_manager_llm(self) -> LLM:
        """Get LLM for crew manager (hierarchical process)"""
        return self.get_analysis_llm()  # Use Claude for strategic coordination
    
    def get_planning_llm(self) -> LLM:
        """Get LLM for planning tasks"""
        return self.get_analysis_llm()  # Use Claude for planning
    
    def test_providers(self) -> Dict[str, bool]:
        """Test all configured providers"""
        results = {}
        
        for provider_name, config in self.providers.items():
            if not config['enabled']:
                results[provider_name] = False
                continue
            
            try:
                # Create test LLM instance
                if provider_name == 'openai':
                    llm = LLM(
                        model=f"openai/{config['model']}",
                        api_key=config['api_key'],
                        base_url=config['base_url']
                    )
                elif provider_name == 'anthropic':
                    llm = LLM(
                        model=f"anthropic/{config['model']}",
                        api_key=config['api_key'],
                        base_url=config['base_url']
                    )
                elif provider_name == 'google':
                    llm = LLM(
                        model=f"google/{config['model']}",
                        api_key=config['api_key'],
                        base_url=config['base_url']
                    )
                elif provider_name == 'deepseek':
                    llm = LLM(
                        model=f"openai/{config['model']}",
                        api_key=config['api_key'],
                        base_url=config['base_url']
                    )
                
                # Test with simple prompt
                response = llm.call("Test connection. Respond with 'OK'.")
                results[provider_name] = "OK" in str(response).upper()
                
            except Exception as e:
                logger.error(f"Provider {provider_name} test failed: {str(e)}")
                results[provider_name] = False
        
        return results

# Global configuration instance
llm_config = LLMConfig()

# Convenience functions for easy access
def get_primary_llm() -> LLM:
    """Get primary LLM instance"""
    return llm_config.get_primary_llm()

def get_analysis_llm() -> LLM:
    """Get analysis LLM instance"""
    return llm_config.get_analysis_llm()

def get_agent_llm(agent_type: str) -> LLM:
    """Get LLM optimized for specific agent type"""
    return llm_config.get_agent_llm(agent_type)

def get_crew_manager_llm() -> LLM:
    """Get crew manager LLM instance"""
    return llm_config.get_crew_manager_llm()

def test_all_providers() -> Dict[str, bool]:
    """Test all configured LLM providers"""
    return llm_config.test_providers()

if __name__ == "__main__":
    # Test configuration when run directly
    print("Testing LLM providers...")
    results = test_all_providers()
    
    for provider, status in results.items():
        status_text = "✅ Working" if status else "❌ Failed"
        print(f"{provider}: {status_text}")
    
    print(f"\nPrimary LLM: {get_primary_llm()}")
    print(f"Analysis LLM: {get_analysis_llm()}")

