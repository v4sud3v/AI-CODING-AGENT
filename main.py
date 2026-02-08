import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from prompts import system_prompt
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ],
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    )

    for _ in range(20):
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

        # Append candidates to conversation history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        if response.function_calls:
            function_results = []  # We'll store the results here for later use
            
            for function_call in response.function_calls:
                # 1. Call the function using your helper
                function_call_result = call_function(function_call, verbose=args.verbose)

                # 2. Validation Ceremony: Check for Parts
                if not function_call_result.parts:
                    raise Exception("Function call result has no parts")
                
                # Grab the first part
                first_part = function_call_result.parts[0]

                # 3. Validation Ceremony: Check for FunctionResponse
                if first_part.function_response is None:
                    raise Exception("The part does not contain a function_response")

                # 4. Validation Ceremony: Check for the actual .response field
                if first_part.function_response.response is None:
                    raise Exception("The function_response does not contain a response field")

                # 5. Success! Add the part to our list
                function_results.append(first_part)

                # 6. Verbose printing
                if args.verbose:
                    print(f"-> {first_part.function_response.response}")
            
            # Append function results to messages
            messages.append(types.Content(role="user", parts=function_results))
        else:
            # No function calls - final response
            print(response.text)
            return
    
    # Max iterations reached without final response
    print("Error: Maximum iterations reached without a final response from the model.")
    sys.exit(1)
main()