import os
import uuid
from gtts import gTTS
from .core_tts_base import AbstractBaseTTS
from ..logger import create_logger

logger = create_logger(__name__)

class GTTSModel(AbstractBaseTTS):
    def __init__(self, model_config: dict) -> None:
        self.output_dir = os.path.abspath("output_audio")
        os.makedirs(self.output_dir, exist_ok=True)
        self.model_config = model_config
        # Allow overriding language and emotion via configuration
        self.language = model_config.get("language", "en")
        self.emotion = model_config.get("emotion", "neutral")
        logger.info("GTTSModel initialized.")

    def generate_speech(self, input_text: str) -> str:
        if not input_text:
            raise ValueError("No input text provided for GTTS conversion.")

        logger.info("Starting TTS conversion using GTTS.")
        unique_filename = f"output_audio_{uuid.uuid4().hex}.wav"
        audio_path = os.path.join(self.output_dir, unique_filename)
        
        # Adjust TTS parameters based on classified emotion
        if self.emotion == "happy":
            slow = False  # Normal fast speed for a cheerful tone
        elif self.emotion == "sad":
            slow = True   # Slow for a melancholic tone
        elif self.emotion == "surprised":
            slow = False  # Normal speed for an excited tone (adjust if needed)
        elif self.emotion == "angry":
            slow = False  # Normal speed, as gTTS does not support intensity adjustments directly
        else:
            slow = False  # Neutral/default tone

        try:
            tts = gTTS(text=input_text, lang=self.language, slow=slow)
            tts.save(audio_path)
            logger.info(f"GTTS conversion successful. Audio saved at {audio_path}")
            return unique_filename
        except Exception as e:
            logger.exception("GTTS conversion failed.")
            raise e
