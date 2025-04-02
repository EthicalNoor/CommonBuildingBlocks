# CommonBuildingBlocks\AI_Innovation_Hub\stt_manager\core_stt_base.py

from abc import ABC, abstractmethod

class AbstractBaseSTT(ABC):
    """Abstract base class for Speech to Text Models (STT)."""
    
    @abstractmethod
    async def generate_text(self, input_audio_file: str, **kwargs):
        pass