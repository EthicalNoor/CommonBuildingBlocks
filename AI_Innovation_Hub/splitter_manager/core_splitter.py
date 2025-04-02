# AI_Innovation_Hub\splitter_engine\core_splitter.py

from abc import ABC, abstractmethod

class AbstractBaseTextSplitter(ABC):
    """Abstract base class for text splitters."""

    @abstractmethod
    def chunkify(self, text: str, chunk_size: int = 25000, chunk_overlap: int = 2500):
        """Splits the given text into chunks with specified size and overlap."""
        pass
