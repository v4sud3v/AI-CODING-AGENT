import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.get_files_info import schema_get_files_info
from prompts import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info],
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = messages,
        config = config
    )

    if response is None or response.usage_metadata is None:
        print("No response received from the model.")
        return
    
    if args.verbose:
        print(f" Prompt Token {response.usage_metadata.prompt_token_count}")
        print(f" Response Token {response.usage_metadata.candidates_token_count}")

    
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)
main()