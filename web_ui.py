"""
Web-based user interface for language detection tool
"""
import os
import sys
import json
import argparse
from flask import Flask, request, render_template, jsonify

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.detector import LanguageDetector
from src.utils import format_confidence

# Initialize Flask app
app = Flask(__name__)

# Initialize language detector
detector = LanguageDetector()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_language():
    """API endpoint to detect language"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data.get('text', '')
    method = data.get('method')
    advanced_cleaning = data.get('advanced_cleaning', False)
    remove_punct = data.get('remove_punct', True)
    remove_nums = data.get('remove_nums', False)
    remove_special = data.get('remove_special', False)
    
    try:
        result = detector.detect(
            text,
            method=method,
            advanced_cleaning=advanced_cleaning,
            remove_punct=remove_punct,
            remove_nums=remove_nums,
            remove_special=remove_special
        )
        
        # Format confidence for display
        result['confidence_formatted'] = format_confidence(result['confidence'])
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Run the web application"""
    parser = argparse.ArgumentParser(description='Run the language detection web interface')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    # Create templates directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    
    # Create index.html template
    with open(os.path.join(os.path.dirname(__file__), 'templates', 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Language Detection Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            min-height: 100px;
            margin-bottom: 15px;
            font-family: inherit;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #2980b9;
        }
        .settings {
            margin: 20px 0;
            padding: 15px;
            background-color: #f0f0f0;
            border-radius: 4px;
        }
        .settings h3 {
            margin-top: 0;
        }
        .settings label {
            display: block;
            margin: 10px 0;
        }
        .settings select {
            padding: 5px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #e8f4fc;
            border-radius: 4px;
            display: none;
        }
        .result h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        .result-item {
            margin-bottom: 10px;
        }
        .result-label {
            font-weight: bold;
        }
        .toggle-settings {
            background: none;
            border: none;
            color: #3498db;
            cursor: pointer;
            padding: 0;
            font-size: 14px;
            margin-bottom: 10px;
            text-decoration: underline;
        }
        .error {
            color: #e74c3c;
            margin-top: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Language Detection Tool</h1>
    
    <div class="container">
        <p>Enter text below to detect its language:</p>
        <textarea id="text-input" placeholder="Type or paste text here..."></textarea>
        
        <button type="button" class="toggle-settings" id="toggle-settings">Show Advanced Settings</button>
        
        <div class="settings" id="settings" style="display: none;">
            <h3>Detection Settings</h3>
            
            <label>
                Detection Method:
                <select id="method">
                    <option value="">Combined (Best Result)</option>
                    <option value="langdetect">Langdetect</option>
                    <option value="textblob">TextBlob</option>
                    <option value="googletrans">Google Translate</option>
                    <option value="spacy">spaCy</option>
                </select>
            </label>
            
            <label>
                <input type="checkbox" id="advanced-cleaning"> 
                Use Advanced Text Cleaning
            </label>
            
            <label>
                <input type="checkbox" id="remove-punct" checked> 
                Remove Punctuation
            </label>
            
            <label>
                <input type="checkbox" id="remove-nums"> 
                Remove Numbers
            </label>
            
            <label>
                <input type="checkbox" id="remove-special"> 
                Remove Special Characters
            </label>
        </div>
        
        <button id="detect-btn">Detect Language</button>
        
        <div class="error" id="error" style="display: none;"></div>
        
        <div class="result" id="result">
            <h3>Detection Results</h3>
            
            <div class="result-item">
                <span class="result-label">Detected Language:</span>
                <span id="language"></span>
            </div>
            
            <div class="result-item">
                <span class="result-label">Language Family:</span>
                <span id="language-family"></span>
            </div>
            
            <div class="result-item">
                <span class="result-label">Confidence:</span>
                <span id="confidence"></span>
            </div>
            
            <div class="result-item">
                <span class="result-label">Is English:</span>
                <span id="is-english"></span>
            </div>
            
            <div class="result-item">
                <span class="result-label">Detection Method:</span>
                <span id="detection-method"></span>
            </div>
            
            <div class="result-item" id="cleaned-text-container" style="display: none;">
                <span class="result-label">Cleaned Text:</span>
                <span id="cleaned-text"></span>
            </div>
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const textInput = document.getElementById('text-input');
            const detectBtn = document.getElementById('detect-btn');
            const methodSelect = document.getElementById('method');
            const advancedCleaningCheckbox = document.getElementById('advanced-cleaning');
            const removePunctCheckbox = document.getElementById('remove-punct');
            const removeNumsCheckbox = document.getElementById('remove-nums');
            const removeSpecialCheckbox = document.getElementById('remove-special');
            const resultDiv = document.getElementById('result');
            const errorDiv = document.getElementById('error');
            const toggleSettingsBtn = document.getElementById('toggle-settings');
            const settingsDiv = document.getElementById('settings');
            const cleanedTextContainer = document.getElementById('cleaned-text-container');
            
            // Toggle settings visibility
            toggleSettingsBtn.addEventListener('click', function() {
                if (settingsDiv.style.display === 'none') {
                    settingsDiv.style.display = 'block';
                    toggleSettingsBtn.textContent = 'Hide Advanced Settings';
                } else {
                    settingsDiv.style.display = 'none';
                    toggleSettingsBtn.textContent = 'Show Advanced Settings';
                }
            });
            
            // Detect language on button click
            detectBtn.addEventListener('click', function() {
                const text = textInput.value.trim();
                
                if (!text) {
                    errorDiv.textContent = 'Please enter some text to detect.';
                    errorDiv.style.display = 'block';
                    resultDiv.style.display = 'none';
                    return;
                }
                
                errorDiv.style.display = 'none';
                
                // Get settings
                const method = methodSelect.value || null;
                const advancedCleaning = advancedCleaningCheckbox.checked;
                const removePunct = removePunctCheckbox.checked;
                const removeNums = removeNumsCheckbox.checked;
                const removeSpecial = removeSpecialCheckbox.checked;
                
                // Send request to API
                fetch('/detect', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        text: text,
                        method: method,
                        advanced_cleaning: advancedCleaning,
                        remove_punct: removePunct,
                        remove_nums: removeNums,
                        remove_special: removeSpecial
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        errorDiv.textContent = data.error;
                        errorDiv.style.display = 'block';
                        resultDiv.style.display = 'none';
                        return;
                    }
                    
                    // Display results
                    document.getElementById('language').textContent = `${data.language} (${data.language_code})`;
                    document.getElementById('language-family').textContent = data.language_family;
                    document.getElementById('confidence').textContent = data.confidence_formatted;
                    document.getElementById('is-english').textContent = data.is_english ? 'Yes' : 'No';
                    document.getElementById('detection-method').textContent = data.method;
                    
                    // Show cleaned text if advanced cleaning is enabled
                    if (advancedCleaning) {
                        document.getElementById('cleaned-text').textContent = data.cleaned_text;
                        cleanedTextContainer.style.display = 'block';
                    } else {
                        cleanedTextContainer.style.display = 'none';
                    }
                    
                    resultDiv.style.display = 'block';
                })
                .catch(error => {
                    errorDiv.textContent = 'An error occurred: ' + error.message;
                    errorDiv.style.display = 'block';
                    resultDiv.style.display = 'none';
                });
            });
        });
    </script>
</body>
</html>""")
    
    print(f"Starting web server on http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
