from flask import Flask, render_template, request, jsonify
import sys
import os
import tempfile
import requests
from gtts import gTTS

app = Flask(__name__, template_folder='templates')

try:
    from playsound import playsound
except Exception:
    playsound = None


def translate_text(text, dest='kn'):
    """Translate text to Kannada using Google Translate API"""
    try:
        params = {
            'client': 'gtx',
            'sl': 'en',
            'tl': dest,
            'dt': 't',
            'q': text
        }
        response = requests.get('https://translate.googleapis.com/translate_a/single', params=params, timeout=10)
        result = response.json()
        
        if result and len(result) > 0:
            translated = result[0][0][0] if result[0] else text
            return translated
        return text
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/')
def home():
    """Serve landing page"""
    return render_template('index.html')


@app.route('/translate', methods=['GET', 'POST'])
def translate():
    """Serve translator page"""
    if request.method == 'POST':
        # API endpoint for translation
        data = request.get_json()
        english_text = data.get('text', '').strip()
        
        if not english_text:
            return jsonify({'error': 'Please enter text to translate'}), 400
        
        kannada_text = translate_text(english_text)
        
        return jsonify({
            'english': english_text,
            'kannada': kannada_text
        })
    
    return render_template('translate.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
