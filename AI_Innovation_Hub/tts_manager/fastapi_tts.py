import os
import uuid
import requests
from .core_tts_base import AbstractBaseTTS
from ..logger import create_logger
from ...core_sys_config import SystemConfiguration as config

logger = create_logger(__name__)

class FastAPITTSModel(AbstractBaseTTS):
    def __init__(self, model_config: dict) -> None:
        self.output_dir = os.path.abspath("output_audio")
        os.makedirs(self.output_dir, exist_ok=True)

        if not model_config:
            logger.error("Model configuration must be provided.")
            raise ValueError("Model configuration cannot be empty.")
        self.fastapi_url = config.FASTAPI_URL
        if not self.fastapi_url:
            logger.error("'fastapi_url' must be provided in the model configuration.")
            raise ValueError("fastapi_url is required in model configuration.")

        self.language = model_config.get("language", "en")
        self.emotion = model_config.get("emotion", "neutral")
        self.model_config = model_config

        logger.info(f"FastAPITTSModel initialized with URL: {self.fastapi_url}")

    def generate_speech(self, input_text: str) -> str:
        if not input_text:
            raise ValueError("No input text provided for TTS conversion.")

        logger.info("Starting TTS conversion using FastAPI TTS service.")
        payload = {
            "text": input_text,
            "emotion": self.emotion,
            "language": self.language
        }
        
        try:
            response = requests.post(self.fastapi_url, json=payload)
            if response.status_code == 200:
                json_response = response.json()
                audio_url = json_response.get("audio_url")
                if not audio_url:
                    raise Exception("FastAPI response did not contain an audio URL")
                # Download the audio file
                audio_response = requests.get(audio_url, stream=True)
                if audio_response.status_code == 200:
                    unique_filename = f"output_audio_{uuid.uuid4().hex}.wav"
                    local_audio_path = os.path.join(self.output_dir, unique_filename)
                    with open(local_audio_path, "wb") as audio_file:
                        for chunk in audio_response.iter_content(chunk_size=1024):
                            audio_file.write(chunk)
                    logger.info(f"Audio file downloaded and saved to {local_audio_path}")
                    return unique_filename
                else:
                    raise Exception("Failed to download audio file from FastAPI")
            else:
                # Provide a clearer message if the endpoint is not found (404)
                if response.status_code == 404:
                    raise Exception("TTS generation failed: Endpoint not found (404). Please verify the FastAPI service URL.")
                else:
                    raise Exception(f"TTS generation failed: {response.text} (Status code: {response.status_code})")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to the FastAPI TTS service: {str(e)}")