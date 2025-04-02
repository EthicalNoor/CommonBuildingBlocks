# AI_Innovation_Hub\embeddings_manager\cohere_embedder.py

from langchain_cohere import CohereEmbeddings
from .core_embedder import AbstractBaseEmbeddingModel
from ..logger import create_logger

logger = create_logger(__name__)

class InitializationError(Exception):
    pass

class CohereEmbeddingProvider(AbstractBaseEmbeddingModel):
    """CohereEmbeddingProvider class implements the AbstractBaseEmbeddingModel interface 
    to provide an embedding model using Cohere."""

    def retrieve_embedding_model(self, model_identifier: str):
        """Initializes and returns a Cohere embedding model instance."""
        return self._initialize_embedding_model(model_identifier)

    def _initialize_embedding_model(self, model_identifier: str):
        try:
            embedding_model = CohereEmbeddings(model=model_identifier)
            logger.info(f"Successfully initialized Cohere embedding model with ID: {model_identifier}")
            return embedding_model

        except Exception as error:
            logger.error(f"Error initializing Cohere embedding model '{model_identifier}': {error}", exc_info=True)
            raise InitializationError(f"Failed to initialize Cohere embedding model: {error}") from error