"""
SAVI — your personal AI assistant.

V2 features (preserved): chat with Gemini, memory system (remember / recall),
time & date tools, calculator.
V3 features (new): SAVI now SPEAKS every response out loud, and you can talk
to it through the microphone. Keyboard input still works too.

Run from the backend folder:
    python main.py

Then type 'voice' to switch to microphone input, 'text' to switch back, or
'exit' to quit.
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from tools import get_time, get_date, calculate, TOOLS
from voice import speak, listen, voice_available

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("SAVI: GEMINI_API_KEY not found.")
    print('Add a line like  GEMINI_API_KEY=your_key  to backend/.env')
    sys.exit(1)

client = genai.Client(api_key=api_key)

# Keep memory.txt in the same folder as main.py so it works no matter which
# directory you run SAVI from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "memory.txt")


# ---------------------------------------------------------------------------
# Memory helpers (V2 feature, preserved)
# ---------------------------------------------------------------------------
def save_memory(text):
    with open(MEMORY_FILE, "a", encoding="utf-8") as file:
        file.write(text + "\n")


def read_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "I don't have any memories yet."


# ---------------------------------------------------------------------------
# Input helpers (V3)
# ---------------------------------------------------------------------------
def get_user_input(use_voice):
    """
    Return the user's input as text. In voice mode this records from the
    microphone; in text mode it reads the keyboard. Voice mode may return
    None (nothing was heard / an error) — the caller handles that.
    """
    if use_voice:
        return listen()
    return input("You: ")


def savi_say(text):
    """Print SAVI's reply and speak it out loud (used everywhere)."""
    print("SAVI:", text)
    speak(text)


# ---------------------------------------------------------------------------
# Main assistant loop
# ---------------------------------------------------------------------------
def main():
    # --- Startup greeting -------------------------------------------------
    greeting = "Hello! I am SAVI, your personal A I assistant."
    print("SAVI:", greeting)
    speak(greeting)

    hint = (
        "You can chat with me, say 'remember' to save something, "
        "'calculate' for math, or ask for the time or date. "
        "Type 'voice' to talk to me, 'text' to type, or 'exit' to quit."
    )
    print("SAVI:", hint)
    speak(hint)

    use_voice = False  # start in keyboard mode (reliable by default)

    while True:
        user_input = get_user_input(use_voice)

        # Voice mode may return None if nothing was heard / an error occurred.
        if not user_input:
            continue

        user_input = user_input.strip()
        cmd = user_input.lower()

        # --- Exit safely --------------------------------------------------
        if cmd in ("exit", "quit", "bye"):
            farewell = "Goodbye! Talk to you soon."
            print("SAVI:", farewell)
            speak(farewell)
            break

        # --- Switch input mode -------------------------------------------
        if cmd == "voice":
            if not voice_available:
                savi_say(
                    "Voice input isn't available. Please install the "
                    "microphone dependencies first."
                )
            else:
                use_voice = True
                savi_say("Voice mode on. Go ahead, I'm listening.")
            continue

        if cmd == "text":
            use_voice = False
            savi_say("Text mode on. You can type to me now.")
            continue

        # --- Remember (memory system) ------------------------------------
        if cmd.startswith("remember "):
            memory = user_input[len("remember "):]
            save_memory(memory)
            savi_say("Memory saved!")
            continue

        # --- Read memory --------------------------------------------------
        # Accept with or without the question mark (speech recognition
        # usually doesn't add punctuation).
        if cmd in ("what do you remember?", "what do you remember"):
            memories = read_memory()
            print("SAVI:")
            print(memories)
            speak(memories)
            continue

        # --- Calculator ---------------------------------------------------
        if cmd.startswith("calculate "):
            expression = user_input[len("calculate "):]
            result = calculate(expression)
            savi_say(result)
            continue

        # --- Keyword tools (time / date) ----------------------------------
        tool_used = False
        for keyword, function in TOOLS.items():
            if keyword in cmd:
                result = function()
                savi_say(result)
                tool_used = True
                break
        if tool_used:
            continue

        # --- Gemini fallback ----------------------------------------------
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input
            )
            savi_say(response.text)
        except Exception:
            savi_say("Gemini is not responding right now. Please try again.")


if __name__ == "__main__":
    main()
