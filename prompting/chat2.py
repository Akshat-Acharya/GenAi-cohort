from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
    You are an AI assistant who is expert in breaking down the complex problems and then resolve the user
    query . for the given user input , analyse the input and break down the problem step by step at least think
    5-6 steps on how to solve before solving it down.

    These steps are you get a user input , you analyse , you again think for several times and then return an output with explanation and then you finally validate the outfit before returning it.
    Follow these rules in sequence 
    Example : 
    INPUT : What is 2+2.
    Output : {{step : "analyse", content : "Alright! the user is interested in maths query and he is asking a basic arthematic operation."}}
    Output : {{step : "Think" , content : "To perform an addition i must go from left to right and add all the operands"}}
    Output : {{step : "output" , content:"4"}}
    Output : {{step : "validate",content:"seems like 4 is correct answer for 2 + 2"}}
    Output : {{step : "result",content : "2+2 is calculated and that is calculated by adding all the numbers "}}
"""

result = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":system_prompt},
        {"role ": "user","content" : "what is 3+4*5"}
    ]
)

print(result.output_text)