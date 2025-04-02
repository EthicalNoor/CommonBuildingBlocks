# AI_Innovation_Hub\embeddings_manager\bedrock_embedder.py

from .core_embedder import AbstractBaseEmbeddingModel
import boto3
from core_sys_config import SystemConfiguration as config
from langchain_community.embeddings import BedrockEmbeddings
from ..logger import create_logger

logger = create_logger(__name__)

class InitializationError(Exception):
    pass

class BedrockEmbeddingProvider(AbstractBaseEmbeddingModel):
    """BedrockEmbeddingProvider class implements the AbstractBaseEmbeddingModel interface 
    to provide an embedding model using AWS Bedrock."""

    def retrieve_embedding_model(self, model_identifier: str):
        """Initializes and returns a Bedrock embedding model instance."""
        return self._fetch_embedding_model(model_identifier)

    def _fetch_embedding_model(self, model_identifier: str):
        try:
            bedrock_client = self._initialize_bedrock_client()
            embedding_model = BedrockEmbeddings(client=bedrock_client, model_id=model_identifier)
            logger.info(f"Successfully initialized Bedrock embedding model with ID: {model_identifier}")
            return embedding_model

        except boto3.exceptions.Boto3Error as error:
            logger.error(f"AWS error for model '{model_identifier}': {error}", exc_info=True)
            raise ConnectionError(f"Failed to connect to AWS Bedrock: {error}") from error

        except Exception as error:
            logger.error(f"Error initializing Bedrock embedding model '{model_identifier}': {error}", exc_info=True)
            raise InitializationError(f"Failed to initialize Bedrock embedding model: {error}") from error

    def _initialize_bedrock_client(self):
        return boto3.client(
            "bedrock-runtime",
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_SECRET_KEY,
            region_name=config.AWS_REGION
        )

