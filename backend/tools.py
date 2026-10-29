from datetime import datetime

def get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p")

def get_date():
    now = datetime.now()
    return now.strftime("%d-%m-%y")

def calculate(expression):
    # Convert spoken math words into symbols so the calculator also works
    # when you speak to SAVI (e.g. "calculate five plus three").
    # Typed input like "calculate 5 + 3" keeps working unchanged.
    expression = expression.lower()
    spoken_math = {
        " plus ": " + ",
        " minus ": " - ",
        " times ": " * ",
        " multiplied by ": " * ",
        " divided by ": " / ",
    }
    for word, symbol in spoken_math.items():
        expression = expression.replace(word, symbol)
    try:
        return str(eval(expression))
    except:
        return "Invalid calculation."
    
TOOLS = {
    "time": get_time,
    "date": get_date,
}