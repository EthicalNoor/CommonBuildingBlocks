# AI_Innovation_Hub\splitter_engine\recursive_engine.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from .core_splitter import AbstractBaseTextSplitter
from ..logger import create_logger

logger = create_logger(__name__)

class RecursiveChunkSplitter(AbstractBaseTextSplitter):
    """Class to split text into chunks using a recursive character-based strategy."""

    def chunkify(self, text_content: str, max_chunk_size: int = 25000, overlap_size: int = 2500) -> list:
        """Split the input text into chunks using RecursiveCharacterTextSplitter."""
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=max_chunk_size,
                chunk_overlap=overlap_size,
                length_function=len,
                is_separator_regex=False
            )
            chunks = text_splitter.create_documents([text_content])
            logger.info(f"Successfully split text into {len(chunks)} chunks.")
            return chunks
        except Exception as error:
            logger.error(f"Exception occurred while splitting text: {error}")
            raise error
