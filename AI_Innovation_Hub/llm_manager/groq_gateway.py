from .core_llm_client import AbstractBaseLLM
import requests
from ...core_sys_config import SystemConfiguration as config
from ..logger import create_logger

logger = create_logger(__name__)

class GroqLLMModel(AbstractBaseLLM):
    """Implementation of the AbstractBaseLLM for the Groq Language Model."""
    
    def __init__(self, model_id: str) -> None:
        if not model_id:
            logger.error(f"Model ID must be provided.")
            raise ValueError("Model ID cannot be empty.")
        
        self.model_id = model_id

        self.api_key = config.GROQ_API_KEY
        self.groq_url = config.GROQ_API_URL
        self.max_tokens = 1000
        self.temperature = 0.9
        
        if not self.api_key:
            logger.error(f"Groq API key is missing in configuration.")
            raise ValueError("Groq API key must be provided.")
        
        logger.info(f"Groq model initialized with ID: {model_id}")
    
    def generate_response(self, prompt: str) -> str:
        """Generates a response from the Groq model based on the provided prompt."""
        if not prompt:
            logger.error(f"Prompt must be provided.")
            raise ValueError("Prompt cannot be empty.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_id,
            "messages": [{"role": "user", "content": prompt}],
            # "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        try:
            logger.info(f"Sending request to Groq API at {self.groq_url}.")
            response = requests.post(self.groq_url, headers=headers, json=payload)
            
            if response.status_code != 200:
                logger.error(
                    f"API call failed with status code {response.status_code}: {response.text}"
                )
                raise RuntimeError(f"Groq API error: {response.status_code}")
            
            data = response.json()
            generated_text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            logger.info(f"Response obtained successfully.")
            return generated_text
        except Exception as error:
            logger.error(
                f"Error generating response from Groq model: {error}"
            )
            raise RuntimeError(f"Failed to generate response from Groq model: {error}") from error
