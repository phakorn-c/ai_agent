import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("Api keys doesn't exist. Please check your api keys.")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    prompt_tokens = 0
    response_tokens = 0
    got_final_response = False

    for iteration in range(20):
        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if response.usage_metadata is None:
            raise RuntimeError("API request failed: usage_metadata is None")

        prompt_tokens += response.usage_metadata.prompt_token_count or 0
        response_tokens += response.usage_metadata.candidates_token_count or 0

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if not response.function_calls:
            got_final_response = True
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")
            print(response.text)
            break

        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            if not function_call_result.parts:
                raise RuntimeError("Function call result has no parts")

            if function_call_result.parts[0].function_response is None:
                raise RuntimeError("Function call result part has no function_response")

            if function_call_result.parts[0].function_response.response is None:
                raise RuntimeError("Function call response has no response field")

            function_responses.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_responses))

    if not got_final_response:
        print(
            f"Error: Maximum iteration limit ({20}) reached without final response from the model."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
