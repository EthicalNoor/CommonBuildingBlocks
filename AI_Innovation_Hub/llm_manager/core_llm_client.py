# CommonBuildingBlocks\AI_Innovation_Hub\llm_gateway\core_llm_client.py

from abc import ABC, abstractmethod

class AbstractBaseLLM(ABC):
    """Abstract base class for Language Models (LLMs). """
    
    @abstractmethod
    def generate_response(self, input_text: str):
        pass