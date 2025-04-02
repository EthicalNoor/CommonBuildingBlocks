# AI_Innovation_Hub\llm_gateway\chat_bedrock_gateway.py

from .core_llm_client import AbstractBaseLLM
import boto3
from ...core_sys_config import SystemConfiguration as config
from langchain_aws import ChatBedrock
from ..logger import create_logger

logger = create_logger(__name__)

class ChatRockLLMModel(AbstractBaseLLM):
    """Implementation of the AbstractBaseLLM for the Chat Bedrock Language Model."""
    
    def __init__(self, model_identifier: str, client=None) -> None:
        if not model_identifier:
            logger.error(f"Model identifier must be provided.")
            raise ValueError("Model identifier cannot be empty.")

        self.client = client if client else self._initialize_chat_bedrock_client()
        self.llm = ChatBedrock(model_id=model_identifier, client=self.client, model_kwargs={"temperature": 0.3, "top_p": 0.9})

    def _initialize_chat_bedrock_client(self):
        """Initializes and returns a Boto3 Chat Bedrock client using AWS credentials from the environment variables."""
        try:
            aws_region = config.AWS_REGION
            if not aws_region:
                logger.error(f"AWS_REGION environment variable not set.")
                raise ValueError("AWS_REGION environment variable must be set.")

            client = boto3.client("bedrock-runtime", region_name=aws_region)
            logger.info(f"Initialized Chat Bedrock client successfully.")
            return client
        except Exception as error:
            logger.error(f"Failed to initialize Chat Bedrock client: {error}")
            raise

    def generate_response(self, input_text: str) -> str:
        """Generates a response from the Chat Bedrock LLM based on the provided input text."""
        if not input_text:
            logger.error(f"Input text must be provided.")
            raise ValueError("Input text cannot be empty.")

        try:
            logger.info(f"Requesting response from Chat Bedrock LLM.")
            response = self.llm.invoke(input_text)
            logger.info(f"Response obtained successfully.")
            return response.content

        except Exception as error:
            logger.error(f"Error obtaining response from Chat Bedrock LLM: {error}")
            raise RuntimeError(f"Failed to generate response from Chat Bedrock LLM: {error}") from error