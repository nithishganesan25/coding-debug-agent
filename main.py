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

def analyze_code(code: str, error: str, mode: str = "debug") -> str:
    """
    Acts as different AI Agents based on the mode requested by the user.
    """
    
    agents = {
        "debug": "You are a Senior Debugging Agent. Find the exact lines causing the error, explain WHY it broke, and rewrite the code flawlessly.",
        "refactor": "You are an Architecture & Refactoring Agent. Analyze the code for performance bottlenecks, bad practices, and messy logic. Rewrite it to be ultra-efficient, pythonic, and elegant.",
        "security": "You are an Elite Application Security Agent. Hunt down vulnerabilities, SQL injections, unprotected variables, or logic flaws in this code. Explain risks and provide a hardened version.",
        "explain": "You are a Technical Teacher. Explain what this code does line-by-line as if I am a junior developer. Focus on making complex concepts incredibly easy to understand."
    }
    
    # Fallback to debug if mode is unknown
    agent_prompt = agents.get(mode, agents["debug"])

    prompt = f"""
    {agent_prompt}
    
    Target Code:
    ```
    {code}
    ```

    Context / Errors (If any):
    ```
    {error}
    ```
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Model Error: {str(e)}\nMake sure you added a valid GEMINI_API_KEY in your .env file."