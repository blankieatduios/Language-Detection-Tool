"""
Language detector module that combines multiple detection methods
"""
import logging
from typing import Dict, List, Tuple, Union, Optional

# Import language detection libraries
from langdetect import detect as langdetect_detect
from langdetect import DetectorFactory
from textblob import TextBlob
from googletrans import Translator

# Import spaCy for language detection
import spacy
try:
    # Try to load the language detector model
    spacy_model = spacy.load("xx_ent_wiki_sm")
    SPACY_AVAILABLE = True
except (OSError, ImportError):
    SPACY_AVAILABLE = False
    spacy_model = None

# Import utility functions
from .utils import clean_text, format_confidence, get_language_name, is_english
from .text_processor import advanced_clean_text, calculate_weighted_confidence, get_language_family

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set seed for reproducibility in langdetect
DetectorFactory.seed = 0


class LanguageDetector:
    """
    Language detector class that combines multiple detection methods
    for more accurate language identification
    """
    
    def __init__(self):
        """Initialize the language detector with available detection methods"""
        self.methods = {
            'langdetect': self._detect_with_langdetect,
            'textblob': self._detect_with_textblob,
            'googletrans': self._detect_with_googletrans,
        }
        
        # Add spaCy if available
        if SPACY_AVAILABLE:
            self.methods['spacy'] = self._detect_with_spacy
        
        # Initialize translator for googletrans
        self.translator = Translator()
        
        logger.info(f"Language detector initialized with methods: {list(self.methods.keys())}")
    
    def _detect_with_langdetect(self, text: str) -> Tuple[str, float]:
        """
        Detect language using langdetect library
        
        Args:
            text: Input text to detect
            
        Returns:
            Tuple of (language_code, confidence)
        """
        try:
            language = langdetect_detect(text)
            # langdetect doesn't provide confidence scores, so we use a default
            return language, 0.8
        except Exception as e:
            logger.warning(f"langdetect detection failed: {e}")
            return "unknown", 0.0
    
    def _detect_with_textblob(self, text: str) -> Tuple[str, float]:
        """
        Detect language using TextBlob library
        
        Args:
            text: Input text to detect
            
        Returns:
            Tuple of (language_code, confidence)
        """
        try:
            blob = TextBlob(text)
            language = blob.detect_language()
            # TextBlob doesn't provide confidence scores, so we use a default
            return language, 0.7
        except Exception as e:
            logger.warning(f"TextBlob detection failed: {e}")
            # Fall back to langdetect if TextBlob fails
            try:
                return langdetect_detect(text), 0.6
            except:
                return "unknown", 0.0
    
    def _detect_with_googletrans(self, text: str) -> Tuple[str, float]:
        """
        Detect language using googletrans library
        
        Args:
            text: Input text to detect
            
        Returns:
            Tuple of (language_code, confidence)
        """
        try:
            detection = self.translator.detect(text)
            return detection.lang, detection.confidence
        except Exception as e:
            logger.warning(f"googletrans detection failed: {e}")
            return "unknown", 0.0
    
    def _detect_with_spacy(self, text: str) -> Tuple[str, float]:
        """
        Detect language using spaCy library
        
        Args:
            text: Input text to detect
            
        Returns:
            Tuple of (language_code, confidence)
        """
        try:
            doc = spacy_model(text)
            language = doc._.language['language']
            confidence = doc._.language['score']
            return language, confidence
        except Exception as e:
            logger.warning(f"spaCy detection failed: {e}")
            return "unknown", 0.0
    
    def detect(self, text: str, method: Optional[str] = None, 
              advanced_cleaning: bool = False, remove_punct: bool = True,
              remove_nums: bool = False, remove_special: bool = False) -> Dict:
        """
        Detect language of input text
        
        Args:
            text: Input text to detect
            method: Specific detection method to use (if None, uses all available methods)
            advanced_cleaning: Whether to use advanced text cleaning
            remove_punct: Whether to remove punctuation during cleaning
            remove_nums: Whether to remove numbers during cleaning
            remove_special: Whether to remove special characters during cleaning
            
        Returns:
            Dictionary with detection results
        """
        if not text or len(text.strip()) == 0:
            return {
                'text': text,
                'language_code': 'unknown',
                'language': 'Unknown',
                'language_family': 'Unknown',
                'is_english': False,
                'confidence': 0.0,
                'method': 'none'
            }
        
        # Clean the text
        if advanced_cleaning:
            cleaned_text = advanced_clean_text(text, remove_punct, remove_nums, remove_special)
        else:
            cleaned_text = clean_text(text)
        
        # If method is specified, use only that method
        if method and method in self.methods:
            language_code, confidence = self.methods[method](cleaned_text)
            language_name = get_language_name(language_code)
            language_family = get_language_family(language_code)
            english = is_english(language_code)
            
            return {
                'text': text,
                'cleaned_text': cleaned_text,
                'language_code': language_code,
                'language': language_name,
                'language_family': language_family,
                'is_english': english,
                'confidence': confidence,
                'method': method
            }
        
        # Use all available methods and combine results
        results = {}
        for method_name, detect_func in self.methods.items():
            try:
                language_code, confidence = detect_func(cleaned_text)
                results[method_name] = {
                    'language_code': language_code,
                    'confidence': confidence
                }
            except Exception as e:
                logger.error(f"Error in {method_name} detection: {e}")
                results[method_name] = {
                    'language_code': 'unknown',
                    'confidence': 0.0
                }
        
        # Calculate weighted confidence and determine best language
        language_code, confidence = calculate_weighted_confidence(results)
        
        # Get language name, family, and check if English
        language_name = get_language_name(language_code)
        language_family = get_language_family(language_code)
        english = is_english(language_code)
        
        # Determine which method contributed most to the result
        method_counts = {}
        for method_result in results.values():
            lang = method_result['language_code']
            if lang == language_code:
                method_name = next((m for m, r in results.items() if r['language_code'] == lang), 'combined')
                method_counts[method_name] = method_counts.get(method_name, 0) + 1
        
        best_method = max(method_counts.items(), key=lambda x: x[1])[0] if method_counts else 'combined'
        
        return {
            'text': text,
            'cleaned_text': cleaned_text,
            'language_code': language_code,
            'language': language_name,
            'language_family': language_family,
            'is_english': english,
            'confidence': confidence,
            'method': best_method,
            'all_results': results
        }
    
    def detect_batch(self, texts: List[str]) -> List[Dict]:
        """
        Detect language for a batch of texts
        
        Args:
            texts: List of input texts to detect
            
        Returns:
            List of dictionaries with detection results
        """
        return [self.detect(text) for text in texts]
