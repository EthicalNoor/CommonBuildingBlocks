# CommonBuildingBlocks\AI_Innovation_Hub\stt_gateway\stt_gateway_factory.py

from .deepgram_stt import DeepgramSTTModel
from ..logger import create_logger
from .stt_configurator import STT_CONFIG

logger = create_logger(__name__)

class STTInstantiationError(Exception):
    def __init__(self, model_type, original_exception):
        super().__init__(f"Failed to instantiate STT model '{model_type}': {original_exception}")

class STTFactory:

    @staticmethod
    def get_stt_model(model_id: str):
        stt_config = STT_CONFIG.get(model_id)
        if stt_config is None:
            error_message = f"Unsupported STT model ID: '{model_id}'"
            logger.error(error_message)
            raise ValueError(error_message)
        
        try:
            invocation_type = stt_config.get("invocation_type")
            if not invocation_type:
                error_message = f"Missing 'invocation_type' for STT model '{model_id}'"
                logger.error(error_message)
                raise ValueError(error_message)
            
            model_class = globals().get(invocation_type)
            if model_class is None:
                error_message = f"Unsupported invocation type '{invocation_type}' for STT model '{model_id}'"
                logger.error(error_message)
                raise ValueError(error_message)
            
            model_identifier = stt_config.get("model") or stt_config.get("version")
            logger.info(f"Initializing STT model '{model_id}' with identifier '{model_identifier}'.")
            return model_class(model_config=stt_config)
        except Exception as e:
            logger.error(f"Failed to instantiate STT model '{model_id}': {e}", exc_info=True)
            raise STTInstantiationError(model_id, e) from e
