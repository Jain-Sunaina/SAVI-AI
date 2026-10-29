"""
SAVI voice module — text-to-speech (TTS) and speech recognition (STT).

V2 had only speak() (text-to-speech with pyttsx3).
V3 adds listen() so you can talk to SAVI through the microphone.

Dependencies:
    pyttsx3            — text-to-speech engine (already installed in V2)
    SpeechRecognition  — converts speech to text
    PyAudioWPatch      — microphone backend (drop-in for the missing
                         'pyaudio' package; ships prebuilt Windows wheels)

Note on PyAudio: SpeechRecognition looks for a module literally called
'pyaudio'. PyAudioWPatch installs under the name 'pyaudiowpatch' instead, so
we register it under 'pyaudio' in sys.modules before importing
SpeechRecognition. If anything is missing, voice_available becomes False and
SAVI simply falls back to keyboard input.
"""

import sys
import pyttsx3

# ---------------------------------------------------------------------------
# Text-to-Speech (existing V2 feature, unchanged)
# ---------------------------------------------------------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 180)   # words per minute


def speak(text):
    """Say the given text out loud (text-to-speech)."""
    engine.say(text)
    engine.runAndWait()


# ---------------------------------------------------------------------------
# Speech recognition (new in V3) — microphone input
# ---------------------------------------------------------------------------
voice_available = False
sr = None
_recognizer = None

try:
    # PyAudioWPatch is an API-compatible drop-in for pyaudio. Register it
    # under the name SpeechRecognition expects.
    import pyaudiowpatch as _pyaudio
    sys.modules["pyaudio"] = _pyaudio

    import speech_recognition as sr
    _recognizer = sr.Recognizer()
    voice_available = True
except Exception:
    # Microphone support is optional. If anything is missing or fails,
    # SAVI still works perfectly with keyboard input.
    voice_available = False


def listen(timeout=5, phrase_time_limit=10):
    """
    Listen for a single phrase from the microphone and return the recognized
    text as a string. Returns None if nothing was heard, the speech was not
    understood, or an error occurred (the caller can react gracefully).

    Uses Google's free speech-to-text service (no API key required for basic
    use; needs an internet connection).
    """
    if not voice_available or _recognizer is None:
        speak("Voice input is not available. Please install the microphone dependencies.")
        return None

    recognizer = _recognizer

    # 1) Capture audio from the microphone.
    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Tune out background noise for better accuracy.
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
    except sr.WaitTimeoutError:
        # The user didn't say anything within the timeout.
        return None
    except Exception as mic_error:
        # Microphone not connected / permission denied / hardware issue.
        print(f"Microphone error: {mic_error}")
        speak("I couldn't access the microphone. Please check your mic settings.")
        return None

    # 2) Convert the captured audio to text.
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        # Speech was heard but not understandable.
        speak("Sorry, I didn't catch that. Could you say it again?")
        return None
    except sr.RequestError:
        # Recognition service unreachable (no internet, etc.).
        speak("I couldn't reach the speech service. Please check your internet connection.")
        return None
    except Exception:
        speak("Something went wrong while recognizing speech.")
        return None
