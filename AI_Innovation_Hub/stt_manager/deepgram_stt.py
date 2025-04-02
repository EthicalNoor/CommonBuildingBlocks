# CommonBuildingBlocks\AI_Innovation_Hub\stt_manager\deepgram_stt.py

import os
import mimetypes
from .core_stt_base import AbstractBaseSTT
from ..logger import create_logger
from ...core_sys_config import SystemConfiguration as config
from deepgram import Deepgram

logger = create_logger(__name__)

class DeepgramSTTModel(AbstractBaseSTT):
    def __init__(self, model_config: dict) -> None:
        if not model_config:
            logger.error("Model configuration must be provided.")
            raise ValueError("Model configuration cannot be empty.")
        try:
            self.deepgram = Deepgram(config.DEEPGRAM_API_KEY)
        except Exception as e:
            logger.error("Error initializing Deepgram client.", exc_info=True)
            raise e
        
        self.model_name = model_config.get("model") or model_config.get("version")
        if not self.model_name:
            logger.error("Missing 'model' and 'version' in configuration.")
            raise ValueError("Model name/version must be specified in the configuration.")
        
        self.model_config = model_config
        logger.info(f"DeepgramSTTModel initialized with model: {self.model_name}")
    
    async def generate_text(self, input_audio_file: str, **kwargs):
        """Transcribes audio using Deepgram's async API."""
        language = kwargs.get("language", "en")
        
        if not os.path.exists(input_audio_file):
            logger.error(f"Audio file '{input_audio_file}' does not exist.")
            raise FileNotFoundError(f"Audio file '{input_audio_file}' not found.")
        
        try:
            file_size = os.stat(input_audio_file).st_size
            logger.info(f"📂 File size: {file_size} bytes")
        except Exception as e:
            logger.exception("Failed to obtain file size for %s", input_audio_file)
            raise e

        mimetype = mimetypes.guess_type(input_audio_file)[0] or "audio/wav"
        
        try:
            with open(input_audio_file, "rb") as audio:
                logger.info("📤 Sending request to Deepgram API...")
                response = await self.deepgram.transcription.prerecorded(
                    {"buffer": audio, "mimetype": mimetype},
                    {
                        "punctuate": True,
                        "model": self.model_name,
                        "smart_format": True,
                        "language": language
                    }
                )
                logger.info("📥 Received response from Deepgram API.")
        except Exception as e:
            logger.error("Error during Deepgram transcription request.", exc_info=True)
            raise e

        transcript = ""
        try:
            if not response:
                logger.error("Empty response received from Deepgram API.")
                return transcript
            
            if not (results := response.get("results")):
                logger.error("No 'results' found in response.")
                return transcript
            
            if not (channels := results.get("channels")):
                logger.error("No 'channels' found in results.")
                return transcript
            
            if not (first_channel := channels[0] if len(channels) > 0 else None):
                logger.error("No data in the first channel.")
                return transcript
            
            if not (alternatives := first_channel.get("alternatives")):
                logger.error("No 'alternatives' found in first channel.")
                return transcript
            
            if not (first_alternative := alternatives[0] if len(alternatives) > 0 else None):
                logger.error("No data in first alternative.")
                return transcript
            
            transcript = first_alternative.get("transcript", "")
            confidence = first_alternative.get("confidence", 0)
            
            if transcript:
                logger.info(f"📝 Transcript: {transcript}")
                logger.info(f"🔍 Confidence: {confidence}")
            else:
                logger.warning("Received empty transcript.")
        except Exception as e:
            logger.error(f"Failed to process response: {e}", exc_info=True)
            raise e

        return transcript