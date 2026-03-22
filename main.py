import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Get the API Key from .env
api_key = os.environ.get("GEMINI_API_KEY", "")

if not api_key or api_key == "paste_your_api_key_here":
    print("Warning: GEMINI_API_KEY is not assigned in .env!")

# Configure the library
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-2.5-flash")

def debug_code(code: str, error: str) -> str:
    prompt = f"""
    You are an expert coding assistant.
    
    Fix the following code and explain the error step-by-step.
    Also give the corrected code.

    Code:
    ```
    {code}
    ```

    Error:
    ```
    {error}
    ```
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Model Error: {str(e)}\nMake sure you added a valid GEMINI_API_KEY in your .env file."