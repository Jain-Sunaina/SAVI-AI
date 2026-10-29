<<<<<<< HEAD
# SAVI AI 🤖

SAVI is a personal AI assistant built with Python and the Gemini API. It can
chat, remember things, do math, tell the time and date, **speak its responses
out loud**, and **listen to you through the microphone**.

## Features

### V3 — Voice Assistant (current)
- Speaks every response out loud (greeting, chat, tools, errors)
- Microphone speech recognition — talk to SAVI instead of typing
- Keyboard input still works too (switch any time)
- Safe exit command
- Graceful handling for mic errors, unrecognized speech, missing
  dependencies, and API failures

### V2 — Smart Tools (preserved)
- Memory system — save and recall information
- Time tool
- Date tool
- Calculator tool (now understands spoken math words like "plus" / "minus")

### V1
- Basic chatbot with Gemini

## Tech Stack
- Python 3.12+
- Google Gemini API (`google-genai`)
- `pyttsx3` for text-to-speech
- `SpeechRecognition` + `PyAudioWPatch` for microphone input
- `python-dotenv` for loading the API key

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or install them individually:

```bash
pip install pyttsx3==2.99 google-genai==2.8.0 python-dotenv==1.2.2 SpeechRecognition==3.17.0 PyAudioWPatch==0.2.12.9
```

> **Note on PyAudio:** The standard `pyaudio` package has no prebuilt wheel for
> very new Python versions on Windows. This project uses `PyAudioWPatch`
> instead, which is an API-compatible drop-in that ships prebuilt Windows
> wheels — no build tools needed.

### 2. Add your Gemini API key

Create `backend/.env` with one line:

```
GEMINI_API_KEY=your_api_key_here
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

### 3. Run SAVI

From the `backend` folder:

```bash
python main.py
```

## How to use

| You type / say | SAVI does |
| --- | --- |
| `hello` | Chatting with Gemini (and speaks the answer) |
| `remember my name is Sunai` | Saves it to memory and confirms out loud |
| `what do you remember?` | Reads back everything it remembers (spoken) |
| `calculate 12 plus 8` | Answers `20` out loud |
| `what time is it` | Tells you the current time (spoken) |
| `what is the date` | Tells you today's date (spoken) |
| `voice` | Switches to **microphone** input |
| `text` | Switches back to **keyboard** input |
| `exit` / `quit` / `bye` | Says goodbye and quits |

### Voice mode
Type `voice` and SAVI will start listening through your microphone. Then just
talk. It prints what it heard and speaks its reply. Type `text` any time to go
back to the keyboard.

> Tip: use headphones so SAVI's own voice doesn't get picked up by the mic.

## Project structure

```
Sunaina-AI/
├── backend/
│   ├── main.py        # Assistant loop (commands, voice/text modes, Gemini)
│   ├── voice.py       # Text-to-speech + microphone speech recognition
│   ├── tools.py       # Calculator, time, date tools
│   ├── memory.txt     # Saved memories (gitignored — private)
│   └── .env           # Gemini API key (gitignored — secret)
├── mobile/            # Future: mobile app
├── requirements.txt
├── .gitignore
└── README.md
```

## Security notes
- The Gemini API key lives only in `backend/.env`, which is gitignored.
- `memory.txt` is gitignored (your private memories are never committed).
- Python cache files are gitignored.

## Version History
- **V3** — Voice Assistant: TTS on all responses + microphone speech
  recognition + voice/keyboard input modes + safe exit + error handling
- **V2** — Memory system, Date & Time tools, Calculator tool
- **V1** — Basic chatbot

## Future Plans
- Wake-word detection ("Hey SAVI")
- Long-Term Memory
- Mobile app
=======
# SAVI-AI
>>>>>>> 1dbf84659ada66165b64fcf927e4c92834c8faf0
