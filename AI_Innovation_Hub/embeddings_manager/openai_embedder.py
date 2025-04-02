# AI_Innovation_Hub\embeddings_manager\openai_embedder.py

from langchain_openai import OpenAIEmbeddings
from .core_embedder import AbstractBaseEmbeddingModel
from ..logger import create_logger

logger = create_logger(__name__)

class InitializationError(Exception):
    """Custom exception for errors during the initialization of embedding models."""
    pass

class OpenAIEmbeddingProvider(AbstractBaseEmbeddingModel):
    """OpenAIEmbeddingProvider class implements the AbstractBaseEmbeddingModel interface 
    to provide an embedding model using OpenAI."""

    def retrieve_embedding_model(self, model_identifier: str):
        """Initializes and returns an OpenAI embedding model instance."""
        return self._initialize_embedding_model(model_identifier)

    def _initialize_embedding_model(self, model_identifier: str):
        """Initializes and returns an OpenAI embedding model instance."""
        try:
            embedding_model = OpenAIEmbeddings(model=model_identifier)
            logger.info(f"Successfully initialized OpenAI embedding model with ID: {model_identifier}")
            return embedding_model

        except Exception as error:
            logger.error(f"Error initializing OpenAI embedding model '{model_identifier}': {error}", exc_info=True)
            raise InitializationError(f"Failed to initialize OpenAI embedding model: {error}") from error