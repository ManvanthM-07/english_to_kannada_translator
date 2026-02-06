#!/usr/bin/env python3
"""
Simple English -> Kannada translator with text-to-speech.

Usage:
  python translator.py         # interactive prompt
  python translator.py "Hello world"  # translate and speak

Dependencies: see requirements.txt
"""
import sys
import os
import tempfile
import requests
from gtts import gTTS

try:
    from playsound import playsound
except Exception:
    playsound = None


def translate_text(text, dest='kn'):
    """Translate text to Kannada using Google Translate API via requests"""
    try:
        # Using a simple translation approach via Google's public API
        from urllib.parse import quote
        url = f"https://translate.googleapis.com/translate_a/element.js?cb=googleTranslateElementInit&src=auto&tld=com"
        
        # Alternative: Use a simpler free translation endpoint
        params = {
            'client': 'gtx',
            'sl': 'en',
            'tl': dest,
            'dt': 't',
            'q': text
        }
        
        response = requests.get('https://translate.googleapis.com/translate_a/single', params=params, timeout=10)
        result = response.json()
        
        # Extract translated text from the response
        if result and len(result) > 0:
            translated = result[0][0][0] if result[0] else text
            return translated
        return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def speak_text(text, lang='kn'):
    """Generate and play audio for the given text"""
    tts = gTTS(text=text, lang=lang, slow=False)
    fd, path = tempfile.mkstemp(suffix='.mp3')
    os.close(fd)
    try:
        tts.save(path)
        if playsound:
            try:
                playsound(path)
            except Exception as e:
                print(f'Could not play audio: {e}')
                print(f'Audio saved to: {path}')
        else:
            print(f'Audio saved to: {path}')
    except Exception as e:
        print(f'Error generating audio: {e}')
    finally:
        try:
            os.remove(path)
        except Exception:
            pass


def interactive():
    print('English -> Kannada translator (type "quit" to exit)')
    while True:
        try:
            text = input('\nEnter English text: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nGoodbye')
            return
        if not text:
            continue
        if text.lower() in ('quit', 'exit'):
            print('Goodbye')
            return
        try:
            print('Translating...')
            kn = translate_text(text)
            print(f'\nKannada: {kn}')
            print('Playing audio...')
            speak_text(kn)
        except Exception as e:
            print('Error:', e)


def main():
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        try:
            print('Translating...')
            kn = translate_text(text)
            print(f'Kannada: {kn}')
            print('Playing audio...')
            speak_text(kn)
        except Exception as e:
            print('Error:', e)
            sys.exit(1)
    else:
        interactive()


if __name__ == '__main__':
    main()

