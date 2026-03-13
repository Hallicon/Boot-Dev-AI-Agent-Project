import os
import argparse
import time
from functions.call_function import *
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt


# Parse any arguments passed into the script
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


# Load environement variables
load_dotenv()
my_api_key = os.environ.get("GEMINI_API_KEY")

if my_api_key is None:
    raise RuntimeError("Unable to acquire api key for Gemini.")

# Create client
client = genai.Client(api_key=my_api_key)

# Create list to store conversation with Gemini
messages = [
    types.Content(
        role="user",
        parts=[types.Part(text=args.user_prompt)]
    )
]


for _ in range(20):
    # Generate the response
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.0,
            tools=[callable_functions]
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # Tokens in the prompt
    prompt_tokens = response.usage_metadata.prompt_token_count
    # Tokens in the response
    response_tokens = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    # The function_calls property of the response contains a list of functions called as a list of FunctionCall
    if response.function_calls:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if function_call_result.parts[0] is None:
                raise Exception("Error in function calling")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Error in function response")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_results))
    else:
        print(f"Response:\n{response.text}")
        break
    time.sleep(2)
