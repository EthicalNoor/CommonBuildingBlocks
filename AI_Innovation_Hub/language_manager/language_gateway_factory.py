# AI_Innovation_Hub/language_gateway/detector_factory.py

from .core_language_detector import AbstractLanguageDetector, DETECTOR_ENGINE
from .language_identifier import LanguageDetectDetector
from ..logger import create_logger

logger = create_logger(__name__)

class LanguageDetectorFactory:
    @staticmethod
    def build_detector() -> AbstractLanguageDetector:
        """
        Constructs and returns a language detector instance based on the configured engine.
        """
        engine = DETECTOR_ENGINE.lower()
        detector_options = {
            "langdetect": LanguageDetectDetector,
        }

        if engine not in detector_options:
            logger.error(f"Invalid detector engine '{engine}' provided. Falling back to 'langdetect'.")
            return LanguageDetectDetector()
        
        logger.info(f"Initializing language detector with engine: '{engine}'.")
        return detector_options[engine]()