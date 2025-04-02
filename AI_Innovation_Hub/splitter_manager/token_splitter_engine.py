# AI_Innovation_Hub\splitter_engine\token_splitter_engine.py

from langchain.text_splitter import TokenTextSplitter
from .core_splitter import AbstractBaseTextSplitter
from ..logger import create_logger

logger = create_logger(__name__)

class TokenChunkSplitter(AbstractBaseTextSplitter):
    """Class to split text into chunks using a token-based strategy."""

    def chunkify(self, text_content: str, max_tokens: int = 25000, overlap_tokens: int = 2500) -> list:
        """Split the input text into chunks using TokenTextSplitter."""
        try:
            text_splitter = TokenTextSplitter(
                chunk_size=max_tokens,
                chunk_overlap=overlap_tokens,
            )
            chunks = text_splitter.create_documents([text_content])
            logger.info(f"Successfully split text into {len(chunks)} chunks.")
            return chunks
        except Exception as error:
            logger.error(f"Exception occurred while splitting text: {error}")
            raise error
