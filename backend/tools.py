from datetime import datetime

def get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p")

def get_date():
    now = datetime.now()
    return now.strftime("%d-%m-%y")

def calculate(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid calculation."
    
TOOLS = {
    "time": get_time,
    "date": get_date,
}