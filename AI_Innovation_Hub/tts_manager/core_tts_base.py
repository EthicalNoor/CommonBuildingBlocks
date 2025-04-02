# CommonBuildingBlocks\AI_Innovation_Hub\stt_gateway\core_stt_base.py

from abc import ABC, abstractmethod

class AbstractBaseTTS(ABC):
    """Abstract base class for Text to Speech Models (TTS). """
    
    @abstractmethod
    def generate_speech(self, input_text: str):
        pass