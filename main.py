import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents = "Why is the sky blue?"
    )

    if response is None or response.usage_metadata is None:
        print("No response received from the model.")
        return
    print(response.text)
    print(f" Prompt Token {response.usage_metadata.prompt_token_count}")
    print(f" Response Token {response.usage_metadata.candidates_token_count}")

main()