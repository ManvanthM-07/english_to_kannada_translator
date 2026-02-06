# english_to_kannada_translator

This project provides a small Python script `translator.py` that translates English text to Kannada and can speak the Kannada output using text-to-speech.

Getting started

1. Create a virtual environment (recommended) and activate it.

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Usage

Interactive mode:

```bash
python translator.py
```

Translate a single phrase and speak:

```bash
python translator.py "Hello, how are you?"
```

Notes

- `gTTS` uses Google's TTS service and requires an internet connection.
- If `playsound` cannot play audio on your system, the script will save the MP3 file and print its path instead.
