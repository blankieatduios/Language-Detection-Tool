"""
Enhanced text processing module for language detection
"""
import re
import string
import unicodedata
from typing import Dict, List, Tuple, Union, Optional

def normalize_text(text: str) -> str:
    """
    Normalize Unicode text by converting to NFKC form
    
    Args:
        text: Input text to normalize
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Normalize Unicode characters
    return unicodedata.normalize('NFKC', text)

def remove_punctuation(text: str) -> str:
    """
    Remove punctuation from text
    
    Args:
        text: Input text
        
    Returns:
        Text without punctuation
    """
    if not text:
        return ""
    
    # Create a translation table to remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def remove_numbers(text: str) -> str:
    """
    Remove numbers from text
    
    Args:
        text: Input text
        
    Returns:
        Text without numbers
    """
    if not text:
        return ""
    
    return re.sub(r'\d+', '', text)

def remove_special_characters(text: str) -> str:
    """
    Remove special characters from text
    
    Args:
        text: Input text
        
    Returns:
        Text without special characters
    """
    if not text:
        return ""
    
    # Keep only letters, numbers, and whitespace
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def advanced_clean_text(text: str, remove_punct: bool = True, 
                       remove_nums: bool = False, 
                       remove_special: bool = False) -> str:
    """
    Advanced text cleaning with configurable options
    
    Args:
        text: Input text to clean
        remove_punct: Whether to remove punctuation
        remove_nums: Whether to remove numbers
        remove_special: Whether to remove special characters
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Normalize Unicode characters
    text = normalize_text(text)
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Optional processing
    if remove_punct:
        text = remove_punctuation(text)
    
    if remove_nums:
        text = remove_numbers(text)
    
    if remove_special:
        text = remove_special_characters(text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def calculate_weighted_confidence(results: Dict[str, Dict]) -> Tuple[str, float]:
    """
    Calculate weighted confidence score from multiple detection methods
    
    Args:
        results: Dictionary of detection results from multiple methods
        
    Returns:
        Tuple of (language_code, confidence)
    """
    if not results:
        return "unknown", 0.0
    
    # Define weights for each method (can be adjusted based on performance)
    method_weights = {
        'langdetect': 0.3,
        'textblob': 0.2,
        'googletrans': 0.3,
        'spacy': 0.4
    }
    
    # Count language occurrences and weighted confidence
    language_scores = {}
    
    for method, result in results.items():
        lang = result.get('language_code', 'unknown')
        conf = result.get('confidence', 0.0)
        
        # Ensure confidence is a float
        if conf is None:
            conf = 0.0
            
        weight = method_weights.get(method, 0.1)
        
        if lang not in language_scores:
            language_scores[lang] = {
                'count': 0,
                'weighted_conf': 0.0
            }
        
        language_scores[lang]['count'] += 1
        language_scores[lang]['weighted_conf'] += conf * weight
    
    # Find language with highest weighted confidence
    if not language_scores:
        return "unknown", 0.0
        
    best_lang = max(language_scores.items(), 
                   key=lambda x: (x[1]['count'], x[1]['weighted_conf']))
    
    lang_code = best_lang[0]
    
    # Normalize confidence to 0-1 range
    total_weight = sum(method_weights.get(m, 0.1) for m in results.keys())
    confidence = best_lang[1]['weighted_conf'] / total_weight if total_weight > 0 else 0.0
    
    return lang_code, min(confidence, 1.0)

def get_language_family(language_code: str) -> str:
    """
    Get language family for a given language code
    
    Args:
        language_code: ISO language code
        
    Returns:
        Language family name
    """
    language_families = {
        # Germanic languages
        'en': 'Germanic',
        'de': 'Germanic',
        'nl': 'Germanic',
        'sv': 'Germanic',
        'no': 'Germanic',
        'da': 'Germanic',
        
        # Romance languages
        'es': 'Romance',
        'fr': 'Romance',
        'it': 'Romance',
        'pt': 'Romance',
        'ro': 'Romance',
        
        # Slavic languages
        'ru': 'Slavic',
        'uk': 'Slavic',
        'pl': 'Slavic',
        'cs': 'Slavic',
        'bg': 'Slavic',
        
        # Indo-Aryan languages
        'hi': 'Indo-Aryan',
        'bn': 'Indo-Aryan',
        'pa': 'Indo-Aryan',
        'gu': 'Indo-Aryan',
        
        # East Asian languages
        'zh': 'Sino-Tibetan',
        'ja': 'Japonic',
        'ko': 'Koreanic',
        
        # Other language families
        'ar': 'Semitic',
        'he': 'Semitic',
        'fi': 'Uralic',
        'hu': 'Uralic',
        'tr': 'Turkic',
        'th': 'Tai-Kadai',
        'vi': 'Austroasiatic',
    }
    
    return language_families.get(language_code.lower().split('-')[0], 'Other')
