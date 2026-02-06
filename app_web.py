from flask import Flask, render_template, request, jsonify, send_file
import io
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


@app.after_request
def add_header(response):
    """Add CORS headers to every request"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    return response


@app.route('/translate', methods=['GET', 'POST', 'OPTIONS'])
@app.route('/translate.html', methods=['GET', 'POST', 'OPTIONS'])
def translate():
    """Serve translator page"""
    if request.method == 'OPTIONS':
        return '', 204
        
    if request.method == 'POST':
        print(f"Received translation request: {request.remote_addr}")
        # API endpoint for translation
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        english_text = data.get('text', '').strip()
        
        if not english_text:
            return jsonify({'error': 'Please enter text to translate'}), 400
        
        kannada_text = translate_text(english_text)
        
        return jsonify({
            'english': english_text,
            'kannada': kannada_text
        })
    
    return render_template('translate.html')


@app.route('/speak')
def speak():
    """Generate audio for the given text and return as a stream"""
    text = request.args.get('text', '').strip()
    lang = request.args.get('lang', 'kn')
    
    if not text:
        return "No text provided", 400
        
    try:
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return send_file(fp, mimetype='audio/mpeg')
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
