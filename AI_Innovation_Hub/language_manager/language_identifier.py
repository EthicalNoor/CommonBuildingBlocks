# AI_Innovation_Hub/language_gateway/langdetect_detector.py

from langdetect import detect, LangDetectException
from .core_language_detector import AbstractLanguageDetector, SAMPLE_TEXT_LENGTH, AVAILABLE_LANGUAGES, USE_FALLBACK_LANGUAGE, FALLBACK_LANGUAGE
from ..logger import create_logger

logger = create_logger(__name__)

class LanguageDetectDetector(AbstractLanguageDetector):
    def identify_language_code(self, text: str) -> str:
        """
        Uses langdetect to identify the language code from the given text.
        If default fallback is enabled or detection fails, returns the fallback language.
        """
        if USE_FALLBACK_LANGUAGE:
            logger.info("Fallback language usage enabled. Returning fallback language.")
            return FALLBACK_LANGUAGE

        try:
            detected = detect(text[:SAMPLE_TEXT_LENGTH])
            base_code = detected.split('-')[0].upper()

            if base_code in AVAILABLE_LANGUAGES:
                logger.info(f"Detected supported language: {base_code}")
                return base_code
            
            logger.warning(f"Unsupported language detected ({base_code}). Using fallback language: {FALLBACK_LANGUAGE}")
            return FALLBACK_LANGUAGE
        
        except LangDetectException as error:
            logger.error(f"Language detection error: {error}", exc_info=True)
            return FALLBACK_LANGUAGE