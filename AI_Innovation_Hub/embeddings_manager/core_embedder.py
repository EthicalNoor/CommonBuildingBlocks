# AI_Innovation_Hub\embeddings_manager\core_embedder.py

from abc import ABC, abstractmethod

class AbstractBaseEmbeddingModel(ABC):
    """Abstract base class for embedding models."""
    
    @abstractmethod
    def retrieve_embedding_model(self, unique_model_id: str):
        pass
