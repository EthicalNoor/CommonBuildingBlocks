# CommonBuildingBlocks\AI_Innovation_Hub\tts_gateway\elevenlabs_tts.py

import os
import uuid
import io
from pydub import AudioSegment
from elevenlabs import ElevenLabs
from elevenlabs.core.api_error import ApiError
from .core_tts_base import AbstractBaseTTS
from ..logger import create_logger
from ...core_sys_config import SystemConfiguration as config

logger = create_logger(__name__)

class ElevenLabsTTSModel(AbstractBaseTTS):

    def __init__(self, model_config: dict) -> None:
        
        self.output_dir = os.path.abspath("output_audio")
        os.makedirs(self.output_dir, exist_ok=True)
        
        if not model_config:
            logger.error("Model configuration must be provided.")
            raise ValueError("Model configuration cannot be empty.")
        
        try:
            self.client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
        except Exception as e:
            logger.error("Error initializing ElevenLabs Model.", exc_info=True)
            raise e
        
        self.model_name = model_config.get("model") or model_config.get("version")
        if not self.model_name:
            logger.error("Missing 'model' or 'version' in configuration.")
            raise ValueError("Model name/version must be specified in the configuration.")
        
        self.model_config = model_config
        logger.info(f"ElevenLabsTTSModel initialized with model: {self.model_name}")

    def generate_speech(self, input_text: str) -> str:

        if not input_text:
            raise ValueError("No input text provided for TTS conversion.")

        logger.info("Starting TTS conversion using ElevenLabs.")
        unique_filename = f"output_audio_{uuid.uuid4().hex}.wav"
        audio_path = os.path.join(self.output_dir, unique_filename)
        
        try:
            audio_stream = self.client.text_to_speech.convert(
                voice_id=config.ELEVENLABS_VOICE_ID,
                model_id=self.model_name,
                text=input_text
            )
            audio_data = b"".join(audio_stream)
            audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_data))
            audio_segment.export(audio_path, format="wav")
            logger.info(f"TTS conversion successful. Audio saved at {audio_path}")
            return unique_filename
        
        except ApiError as e:
            if e.status_code == 401:
                logger.exception("Unauthorized access detected. Please check your subscription or API usage")
                raise  ApiError(status_code=401, body={"detail": "Free Tier usage disabled."})
            else:
                raise e
        
        except Exception as e:
            logger.exception("TTS conversion failed.")
            raise e