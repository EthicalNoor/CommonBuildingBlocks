# AI_Innovation_Hub/language_gateway/base_detector.py

from abc import ABC, abstractmethod
from ...core_sys_config import SystemConfiguration as config

# Mapping for language codes to full names
LANGUAGE_MAP = {
    'EN': 'English',
    'FR': 'French',
    'ES': 'Spanish',
    'DE': 'German',
    'IT': 'Italian',
    'PT': 'Portuguese',
    'RU': 'Russian',
    'ZH': 'Chinese',
    'JA': 'Japanese',
    'KO': 'Korean',
    'HI': 'Hindi'
}

# Available language codes
AVAILABLE_LANGUAGES = list(LANGUAGE_MAP.keys())

# Configuration constants
SAMPLE_TEXT_LENGTH = 400
DETECTOR_ENGINE = 'langdetect'
USE_FALLBACK_LANGUAGE = config.USE_DEFAULT_LANG
FALLBACK_LANGUAGE = config.DEFAULT_LANG

class AbstractLanguageDetector(ABC):
    @abstractmethod
    def identify_language_code(self, text: str) -> str:
        """
        Identifies and returns a language code based on the provided text.
        """
        pass

    def resolve_language_name(self, code: str) -> str:
        """
        Returns the full language name for a given code. Defaults to fallback language if not found.
        """
        base_code = code.split('-')[0].upper()
        return LANGUAGE_MAP.get(base_code, FALLBACK_LANGUAGE)

    def list_supported_languages(self) -> list:
        """
        Returns the list of supported language codes.
        """
        return AVAILABLE_LANGUAGES