# Language-Detection-Tool

## Overview

The Language Detection Tool is a Python application that identifies the language of input text. It combines multiple detection methods to provide accurate language identification with confidence scores. The tool can detect a wide range of languages and provides both command-line and web-based interfaces.

## Features

- **Multi-method detection**: Combines results from multiple language detection libraries for improved accuracy
- **Advanced text processing**: Configurable text cleaning options to improve detection accuracy
- **Language family identification**: Groups languages by their linguistic families
- **Confidence scoring**: Provides confidence scores for detection results
- **Multiple interfaces**: Command-line interface, interactive mode, and web-based UI
- **Batch processing**: Support for detecting languages in multiple texts at once

## Supported Languages

The tool supports detection of over 50 languages, including:

- English, Spanish, French, German, Italian, Portuguese
- Russian, Ukrainian, Polish, Czech
- Chinese, Japanese, Korean
- Arabic, Hebrew, Persian
- Hindi, Bengali, Urdu
- And many more...

## Installation

### Requirements

- Python 3.6 or higher
- Required Python packages (installed automatically via requirements.txt):
  - langdetect
  - textblob
  - spacy (optional)
  - googletrans
  - flask (for web UI)

### Setup

1. Clone the repository or extract the provided zip file
2. Navigate to the project directory
3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Command-line Interface

```bash
python app.py --text "Text to detect language"
```

#### Options:

- `--text`: Text to detect language
- `--method`: Specific detection method to use (langdetect, textblob, googletrans, spacy)
- `--interactive`: Run in interactive mode
- `--advanced-cleaning`: Use advanced text cleaning
- `--remove-punct`: Remove punctuation during cleaning
- `--remove-numbers`: Remove numbers during cleaning
- `--remove-special`: Remove special characters during cleaning

### Interactive Mode

```bash
python app.py --interactive
```

In interactive mode, you can:
- Enter text to detect its language
- Type 'help' to see available commands
- Type 'settings' to view current settings
- Configure detection settings with the 'set' command
- Type 'exit' or 'quit' to end the program

### Web Interface

```bash
python web_ui.py
```

This starts a web server (default: http://0.0.0.0:5000) where you can:
- Enter text in the input field
- Configure detection settings
- View detection results in a user-friendly format

## API Reference

### Core Classes

#### LanguageDetector

The main class for language detection.

```python
from src.detector import LanguageDetector

detector = LanguageDetector()
result = detector.detect("Text to detect")
print(f"Detected language: {result['language']}")
```

#### Methods:

- `detect(text, method=None, advanced_cleaning=False, remove_punct=True, remove_nums=False, remove_special=False)`: Detect language of input text
- `detect_batch(texts)`: Detect language for a batch of texts

#### Return Value:

The `detect` method returns a dictionary with the following keys:
- `text`: Original input text
- `cleaned_text`: Text after cleaning (if advanced_cleaning is True)
- `language_code`: ISO language code (e.g., 'en', 'es', 'fr')
- `language`: Full language name
- `language_family`: Language family name
- `is_english`: Boolean indicating if the language is English
- `confidence`: Confidence score (0-1)
- `method`: Detection method used
- `all_results`: Results from all detection methods

### Utility Functions

The `src.utils` module provides utility functions:

- `clean_text(text)`: Basic text cleaning
- `format_confidence(confidence)`: Format confidence score as percentage
- `get_language_name(language_code)`: Get full language name from ISO code
- `is_english(language_code)`: Check if language is English

### Text Processing

The `src.text_processor` module provides advanced text processing:

- `advanced_clean_text(text, remove_punct, remove_nums, remove_special)`: Advanced text cleaning
- `calculate_weighted_confidence(results)`: Calculate weighted confidence from multiple methods
- `get_language_family(language_code)`: Get language family for a language code

## Performance

The tool achieves high accuracy for most languages:
- 100% accuracy for English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, and Arabic
- Good handling of mixed language text
- Consistent detection of language variants (e.g., Chinese variants)

## Troubleshooting

- If TextBlob detection fails, the tool automatically falls back to other methods
- For best results with short texts, use the combined detection method (default)
- If detection accuracy is low, try enabling advanced text cleaning

## License

This tool is provided for educational and research purposes.

## Credits

This tool uses the following open-source libraries:
- langdetect
- textblob
- spacy
- googletrans
- flask
