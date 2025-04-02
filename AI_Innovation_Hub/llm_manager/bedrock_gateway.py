# CommonBuildingBlocks\AI_Innovation_Hub\llm_gateway\bedrock_gateway.py

from langchain_aws import BedrockLLM
from .core_llm_client import AbstractBaseLLM
from ...core_sys_config import SystemConfiguration as config
import boto3
from ..logger import create_logger

logger = create_logger(__name__)

class BedrockLLMModel(AbstractBaseLLM):
    """Implementation of the AbstractBaseLLM for the Bedrock Language Model."""

    def __init__(self, model_identifier: str, client=None) -> None:
        """Initializes the Bedrock LLM Model with the specified model identifier and optional client."""
        if not model_identifier:
            logger.error(f"Model identifier must be provided.")
            raise ValueError("Model identifier cannot be empty.")
        
        self.client = client if client else self._initialize_bedrock_client()
        self.llm = BedrockLLM(model_id=model_identifier, client=self.client, model_kwargs={'temperature': 0.3, 'top_p': 0.9})

    def _initialize_bedrock_client(self):
        """Initializes and returns a Boto3 Bedrock client using AWS credentials from the environment variables."""
        try:
            aws_region = config.AWS_REGION
            if not aws_region:
                logger.error(f"AWS_REGION environment variable not set.")
                raise ValueError("AWS_REGION environment variable must be set.")
                
            client = boto3.client("bedrock-runtime", region_name=aws_region)
            logger.info(f"Initialized Bedrock client successfully.")
            return client
        except Exception as error:
            logger.error(f"Failed to initialize Bedrock client: {error}")
            raise

    def generate_response(self, input_text: str) -> str:
        """Generates a response from the Bedrock LLM based on the provided input text."""
        if not input_text:
            logger.error(f"Input text must be provided.")
            raise ValueError("Input text cannot be empty.")

        try:
            logger.info(f"Requesting response from Bedrock LLM.")
            response = self.llm.predict(input_text)
            logger.info(f"Response obtained successfully.")
            return response.content
        
        except Exception as error:
            logger.error(f"Error obtaining response from Bedrock LLM: {error}")
            raise RuntimeError(f"Failed to generate response from Bedrock LLM: {error}") from error
