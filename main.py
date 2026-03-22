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

def get_agent_prompt(mode: str) -> str:
    agents = {
        "debug": "You are a Senior Debugging Agent. Find the exact lines causing the error, explain WHY it broke, and rewrite the code flawlessly.",
        "refactor": "You are an Architecture & Refactoring Agent. Analyze the code for performance bottlenecks, bad practices, and messy logic. Rewrite it to be ultra-efficient, pythonic, and elegant.",
        "security": "You are an Elite Application Security Agent. Hunt down vulnerabilities, SQL injections, unprotected variables, or logic flaws in this code. Explain risks and provide a hardened version.",
        "explain": "You are a Technical Teacher. Explain what this code does line-by-line as if I am a junior developer. Focus on making complex concepts incredibly easy to understand."
    }
    return agents.get(mode, agents["debug"])

def analyze_code_stream(code: str, error: str, mode: str = "debug"):
    """
    Acts as different AI Agents based on the mode requested by the user, and streams the result token by token!
    """
    prompt = f"{get_agent_prompt(mode)}\n\nTarget Code:\n```\n{code}\n```\n\nContext / Errors:\n```\n{error}\n```"

    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Model Error:** {str(e)}\nMake sure you added a valid GEMINI_API_KEY."