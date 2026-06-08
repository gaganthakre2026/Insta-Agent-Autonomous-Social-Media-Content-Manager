"""LLM client for Ollama/LLaMA integration."""
import requests
from typing import Optional
from config import settings
import logging

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama and LLaMA models."""
    
    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL, model: str = settings.OLLAMA_MODEL):
        """Initialize Ollama client."""
        self.base_url = base_url
        self.model = model
        self.generate_endpoint = f"{base_url}/api/generate"
    
    def generate(self, prompt: str, stream: bool = False, **kwargs) -> Optional[str]:
        """Generate text using LLaMA."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream,
                **kwargs
            }
            
            response = requests.post(self.generate_endpoint, json=payload, timeout=60)
            response.raise_for_status()
            
            if stream:
                # For streaming, collect all responses
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        import json
                        data = json.loads(line)
                        full_response += data.get("response", "")
                return full_response
            else:
                # Single response
                import json
                result = response.json()
                return result.get("response", "")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


# Global instance
ollama_client = OllamaClient()
