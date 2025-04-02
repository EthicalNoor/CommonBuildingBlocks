# AI_Innovation_Hub\splitter_engine\splitter_factory.py
from .core_splitter import AbstractBaseTextSplitter
from .token_splitter_engine import TokenChunkSplitter
from .recursive_engine import RecursiveChunkSplitter
from ..logger import create_logger

logger = create_logger(__name__)

class SplitterInstantiationError(Exception):
    """Custom exception for errors during the text splitter instantiation."""
    
    def __init__(self, splitter_type, original_exception):
        super().__init__(f"Failed to instantiate splitter '{splitter_type}': {original_exception}")

class SplitterFactory:
    """Factory class for creating instances of text splitters based on specified types."""

    @staticmethod
    def create_text_splitter(splitter_type: str) -> AbstractBaseTextSplitter:
        """Creates a text splitter instance based on the specified splitter type."""
        model_dispatcher = {
            "token": TokenChunkSplitter,
            "recursive": RecursiveChunkSplitter
        }

        try:
            splitter_class = model_dispatcher.get(splitter_type.lower())
            if splitter_class:
                logger.info(f"Initializing '{splitter_type}' text splitter.")
                return splitter_class()
            else:
                error_message = f"Unknown text splitter type: '{splitter_type}'"
                logger.error(error_message)
                raise ValueError(error_message)

        except Exception as error:
            logger.error(f"Failed to instantiate text splitter for '{splitter_type}': {error}", exc_info=True)
            raise SplitterInstantiationError(splitter_type, error) from error