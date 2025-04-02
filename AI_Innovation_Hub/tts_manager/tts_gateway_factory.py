# CommonBuildingBlocks\AI_Innovation_Hub\tts_gateway\tts_gateway_factory.py

from .elevenlabs_tts import ElevenLabsTTSModel
# from .coqui_tts import CoquiTTSModel
# from .style_tts import StyleTTSModel
from .gtts_tts import GTTSModel
from .fastapi_tts import FastAPITTSModel
from ..logger import create_logger
from .tts_configurator import TTS_CONFIG
import copy

logger = create_logger(__name__)

class ttsInstantiationError(Exception):
    def __init__(self, model_type, original_exception):
        super().__init__(f"Failed to instantiate tts model '{model_type}': {original_exception}")

class TTSFactory:

    @staticmethod
    def get_tts_model(model_id: str, **kwargs):
        tts_config = TTS_CONFIG.get(model_id)
        if tts_config is None:
            error_message = f"Unsupported tts model ID: '{model_id}'"
            logger.error(error_message)
            raise ValueError(error_message)
        
        try:
            # Create a deep copy of the configuration to avoid modifying the global TTS_CONFIG.
            config_copy = copy.deepcopy(tts_config)
            # Merge additional parameters into the configuration.
            if kwargs:
                config_copy.update(kwargs)
            
            invocation_type = config_copy.get("invocation_type")
            if not invocation_type:
                error_message = f"Missing 'invocation_type' for tts model '{model_id}'"
                logger.error(error_message)
                raise ValueError(error_message)
            
            model_class = globals().get(invocation_type)
            if model_class is None:
                error_message = f"Unsupported invocation type '{invocation_type}' for tts model '{model_id}'"
                logger.error(error_message)
                raise ValueError(error_message)
            
            model_identifier = config_copy.get("model") or config_copy.get("version")
            logger.info(f"Initializing tts model '{model_id}' with identifier '{model_identifier}'.")
            return model_class(model_config=config_copy)
        except Exception as e:
            logger.error(f"Failed to instantiate tts model '{model_id}': {e}", exc_info=True)
            raise ttsInstantiationError(model_id, e) from e