# AI_Innovation_Hub\text_refiner\text_refiner_engine.py

import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from ..logger import create_logger

# Download NLTK resources if not already downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

logger = create_logger(__name__)

class TextRefinerError(Exception):
    """Custom exception for errors occurring in the TextRefiner process."""
    pass

class TextRefiner:
    """Class to handle text refinement processes including preprocessing and normalization."""

    _lemmatizer = WordNetLemmatizer()
    _stop_words = set(stopwords.words('english'))

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean the input text by removing extra spaces, URLs, and non-alphanumeric characters."""
        text = re.sub(r'https?://\S+|http://\S+|www\.\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.lower()

    @staticmethod
    def _tokenize_and_lemmatize(text: str) -> str:
        """Tokenize and lemmatize the input text."""
        words = nltk.word_tokenize(text)
        lemmatized_words = [
            TextRefiner._lemmatizer.lemmatize(word) for word in words if word not in TextRefiner._stop_words
        ]
        return ' '.join(lemmatized_words)

    @staticmethod
    def refine_text(text: str) -> str:
        """Refine the input text by cleaning, tokenizing, and lemmatizing."""
        try:
            cleaned_text = TextRefiner._clean_text(text)
            refined_text = TextRefiner._tokenize_and_lemmatize(cleaned_text)
            
            logger.info("Successfully refined text.")
            return refined_text
        except Exception as error:
            logger.exception("Error refining text")
            raise TextRefinerError(f"Failed to refine text: {error}") from error