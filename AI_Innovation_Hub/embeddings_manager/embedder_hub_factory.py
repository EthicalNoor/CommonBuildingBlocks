# AI_Innovation_Hub\embeddings_manager\embedder_hub_factory.py

from .core_embedder import AbstractBaseEmbeddingModel
from .bedrock_embedder import BedrockEmbeddingProvider
from .cohere_embedder import CohereEmbeddingProvider
from .openai_embedder import OpenAIEmbeddingProvider
from ..logger import create_logger

logger = create_logger(__name__)

class ModelInstantiationError(Exception):
    """Custom exception for errors during the embedding model instantiation."""
    
    def __init__(self, embedding_model_type, original_exception):
        super().__init__(f"Failed to instantiate model '{embedding_model_type}': {original_exception}")

class EmbeddingModelFactory:
    """Factory class for creating instances of embedding models based on specified types."""

    @staticmethod
    def create_embedding_model(model_type: str, **options) -> AbstractBaseEmbeddingModel:
        """Creates an embedding model instance based on the specified model type."""
        model_mapping = {
            "cohere": CohereEmbeddingProvider,
            "openai": OpenAIEmbeddingProvider,
            "bedrock": BedrockEmbeddingProvider
        }

        try:
            model_class = model_mapping.get(model_type.lower())
            if model_class:
                logger.info(f"Initializing '{model_type}' embedding model.")
                return model_class(**options)
            else:
                error_message = f"Unknown embedding model type: '{model_type}'"
                logger.error(error_message)
                raise ValueError(error_message)

        except Exception as error:
            logger.error(f"Failed to instantiate embedding model for '{model_type}': {error}", exc_info=True)
            raise ModelInstantiationError(model_type, error) from error
