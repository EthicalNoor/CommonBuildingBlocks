# AI_Innovation_Hub\llm_gateway\gemini_gateway.py

from .core_llm_client import AbstractBaseLLM
import google.generativeai as genai
from ...core_sys_config import SystemConfiguration as config
from ..logger import create_logger

logger = create_logger(__name__)

gemini_key = config.GEMINI_API_KEY
genai.configure(api_key=gemini_key)

class GeminiLLMModel(AbstractBaseLLM):
    """Implementation of the AbstractBaseLLM for the Google Gemini Language Model."""
    
    def __init__(self, model_id: str) -> None:
        if not model_id:
            logger.error(f"Model ID must be provided.")
            raise ValueError("Model ID cannot be empty.")

        self.model = self._initialize_gemini_model(model_id)
        logger.info(f"Gemini model initialized with ID: {model_id}")

    def _initialize_gemini_model(self, model_id: str):
        """Initializes and returns the Gemini Generative Model using the provided model ID."""
        try:
            model = genai.GenerativeModel(model_id)
            logger.info(f"Gemini model initialized successfully.")
            return model
        except Exception as error:
            logger.error(f"Failed to initialize Gemini model: {error}")
            raise

    def generate_response(self, input_text: str) -> str:
        """Generates a response from the Gemini model based on the provided input text."""
        if not input_text:
            logger.error(f"Input text must be provided.")
            raise ValueError("Input text cannot be empty.")

        try:
            logger.info(f"Requesting response from Gemini model.")
            response = self.model.generate_content(input_text)
            logger.info(f"Response obtained successfully.")
            return response.text.strip()

        except Exception as error:
            logger.error(f"Error obtaining response from Gemini model: {error}")
            raise RuntimeError(f"Failed to generate response from Gemini model: {error}") from error
