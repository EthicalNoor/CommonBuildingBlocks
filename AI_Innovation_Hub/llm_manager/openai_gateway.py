# AI_Innovation_Hub\llm_gateway\openai_gateway.py

from .core_llm_client import AbstractBaseLLM
import openai
from ..logger import create_logger
from ...core_sys_config import SystemConfiguration as config

logger = create_logger(__name__)

class OpenaiLLMModel(AbstractBaseLLM):
    """Implementation of the AbstractBaseLLM for OpenAI's Chat Completion API."""

    def __init__(self, model_id: str) -> None:
        """Initializes the OpenAI model with the specified model identifier."""
        if not model_id:
            logger.error(f"Model ID must be provided.")
            raise ValueError("Model ID cannot be empty.")

        self.model_id = model_id
        self.client = self._initialize_openai_client()

    def _initialize_openai_client(self):
        """Initializes and returns the OpenAI client using the API key from the configuration."""
        try:
            openai.api_key = config.OPENAI_API_KEY
            openai.api_type = "openai"
            logger.info(f"OpenAI client initialized successfully.")
        except Exception as error:
            logger.error(f"Failed to initialize OpenAI client: {error}")
            raise

    def generate_response(self, input_text: str) -> str:
        """Generates a response from the OpenAI model based on the provided input text."""
        if not input_text:
            logger.error(f"Input text must be provided.")
            raise ValueError("Input text cannot be empty.")

        try:
            logger.info(f"Requesting response from OpenAI model.")
            response = openai.ChatCompletion.create(
                model=self.model_id,
                messages=[{"role": "user", "content": input_text}],
                temperature=0.7
            )
            logger.info(f"Response obtained successfully.")
            return response["choices"][0]["message"]["content"].strip()

        except Exception as error:
            logger.error(f"Error obtaining response from OpenAI model: {error}")
            raise RuntimeError(f"Failed to generate response from OpenAI model: {error}") from error