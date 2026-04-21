import json
import os

from dotenv import load_dotenv
import google.generativeai as genai
import requests

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_weather(city : str):
    print(f"Tool Called : get_weather {city}")
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went Wrong"

def run_command(command):
    result = os.system(command)
    return result


available_tools = {
    "get_weather" : {
        "fn" : get_weather,
        "description":"Takes a city name as an input and return the current weather for the city "
    },
     "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }
}

system_prompt = f"""
    You are an helpfull AI Assitant who is specialized in resolving user query.
    you work on start, plan,action,observe mode.
    For the given user query and available tools,plan the step by step execution, based on the planning,
    select the relevant tool from the available tools.and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules :
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query 

    Output JSON Format :
    {{
        "step" : "string",
        "content":"string",
        "function":"The name of the function if the step is action",
        "input" : "The input parameter for the function"
    }}

    Available Tools :
    - get_weather : Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns ouput

    Example:
    User query : What is the weather of the new york?
    Output : {{"step":"plan","content":"The user is interested in weather data of new york"}}
    Output : {{"step":"plan","content":"From the available tools I should call get_weather"}}
    Output : {{"step":"action","function":"get_weather","input":"new york"}}
    Output : {{"step":"observe","output":"12 Degree Cel"}}
    Output : {{"step":"output","content":"The Weather for new york seems to be 12 degrees."}}
"""

messages = [
     {"role":"system","content":system_prompt},
]

user_query = input('> ')
messages.append({"role":"user","content":user_query})

# 👉 helper to convert messages → single prompt (Gemini style)
def build_prompt(messages):
    prompt = ""
    for msg in messages:
        prompt += f"{msg['role'].upper()}: {msg['content']}\n"
    return prompt

while True : 
    response = model.generate_content(
        build_prompt(messages)
    )

    raw_text = response.text.strip()

    try:
        parsed_output = json.loads(raw_text)
    except:
        print("❌ Invalid JSON from model:\n", raw_text)
        break

    messages.append({"role":"assistant","content":json.dumps(parsed_output)})

    if parsed_output.get("step") == 'plan':
        print(f"🌟 : {parsed_output.get('content')}")
        continue

    if parsed_output.get("step") == 'action':
        tool_name = parsed_output.get("function")
        tool_input = parsed_output.get("input")

        if available_tools.get(tool_name,False) != False:
            output = available_tools[tool_name].get("fn")(tool_input)
            messages.append({
                "role":"assistant",
                "content":json.dumps({"step":"observe","output":output})
            })
            continue

    if parsed_output.get("step") == "output" : 
        print(f"🌟 : {parsed_output.get('content')}")
        break