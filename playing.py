from typing import Dict
from openai import OpenAI
from dotenv import dotenv_values
import json
# import dotenv

config = dotenv_values(".env")

openai_key = config.get("OPENAI_KEY")

if not openai_key:
    raise ValueError("No OPENAI_KEY key found in .env file")

client = OpenAI(
    api_key=openai_key,
)

def update_message_history(history: Dict, new_message: str, role: bool):
    new_message = {"role": role, "content": new_message} 
    history.append(new_message)

def turn_on_lights():
    """Turns on the lights."""
    print("*LIGHTS ON*")

my_custom_functions = [
    {
        'name': 'turn_on_lights',
        'description': 'Turns on the lights.',
        'parameters': {}  # This function does not require any parameters
    }
]



def commandline_chat():
    history = [
    {"role": "system", 
     "content": "You are a helpful assistant."},
    ]
    while True:
        user_msg = input("User: ")

        update_message_history(
            history=history,
            new_message=user_msg,
            role="user"
        )

        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=history,
        #     functions = my_custom_functions,
        #     function_call = 'auto'
        # )
        response = client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages = history,
            functions = my_custom_functions,
            function_call = 'auto'
        ).choices[0].message

            # Checking to see that a function call was invoked
        if response.function_call is not None:

            # Checking to see which specific function call was invoked
            function_called = response.function_call.name

            # Extracting the arguments of the function call
            function_args = json.loads(response.function_call.arguments)

            # Invoking the proper functions
            if function_called == 'turn_on_lights':
                turn_on_lights(*list(function_args.values()))
            
        ai_response = response.content

        print(f"ANGRY AI: {ai_response}")

        update_message_history(
            history=history,
            new_message=ai_response,
            role="assistant"
        )

commandline_chat()