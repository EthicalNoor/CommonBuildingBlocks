# AI_Innovation_Hub\llm_gateway\llm_gateway_factory.py
from .groq_gateway import GroqLLMModel
from .bedrock_gateway import BedrockLLMModel
from .chat_bedrock_gateway import ChatRockLLMModel
from .gemini_gateway import GeminiLLMModel
from .openai_gateway import OpenaiLLMModel
from ..logger import create_logger
from .llm_configurator import LLM_CONFIG

logger = create_logger(__name__)

class ModelInstantiationError(Exception):
    """Custom exception for errors during the LLM model instantiation."""
    
    def __init__(self, model_type, original_exception):
        super().__init__(f"Failed to instantiate model '{model_type}': {original_exception}")

class LLMFactory:
    """Factory class for creating instances of LLM models based on specified model IDs."""

    @staticmethod
    def get_llm_model(model_id: str):
        """Creates an LLM model instance based on the specified model ID."""
        llm_object = LLM_CONFIG.get(model_id)
        
        if not llm_object:
            error_message = f"Unsupported LLM model ID: '{model_id}'"
            logger.error(error_message)
            raise ValueError(error_message)

        try:
            model_class = globals().get(llm_object.get("invocation_type"))
            if model_class:
                model_identifier = llm_object.get("model") or llm_object.get("version")
                logger.info(f"Initializing LLM model '{model_id}' with version '{model_identifier}'.")
                return model_class(model_id=model_identifier)
            else:
                error_message = f"Unsupported invocation type for model '{model_id}'"
                logger.error(error_message)
                raise ValueError(error_message)

        except Exception as error:
            logger.error(f"Failed to instantiate LLM model '{model_id}': {error}", exc_info=True)
            raise ModelInstantiationError(model_id, error) from error