import os
from dotenv import load_dotenv
from google import genai
from tools import get_time, get_date, calculate, TOOLS

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def save_memory(text):
    with open("memory.txt", "a") as file:
        file.write(text + "\n")

def read_memory():
    with open("memory.txt", "r") as file:
        return file.read()

while True:
    user_input = input("You: ")

    if user_input.startswith("remember "):
        memory = user_input.replace("remember ", "")
        save_memory(memory)
        print("SAVI: Memory saved! 🧠")
        continue

    if user_input.lower() == "what do you remember?":
        print("SAVI:")
        print(read_memory())
        continue

    # if "time" in user_input.lower():
    #     print("SAVI:", get_time())
    #     continue
    
    # if "date" in user_input.lower():
    #     print("SAVI :", get_date())
    #     continue
    
    if user_input.lower().startswith("calculate "):
        expression = user_input.replace("calculate ", "")
        print("SAVI:", calculate(expression))
        continue

    tool_used = False

    for keyword, function in TOOLS.items():
        if keyword in user_input.lower():
            print("SAVI:", function())
            tool_used = True
            break
    if tool_used:
        continue

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )

        print("SAVI:", response.text)

    except Exception:
        print("SAVI: Yrrr Gemini server busy hai 😭")
        
