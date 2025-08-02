import os
from googleapiclient import discovery
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Get the API key from the environment variables
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please set the GEMINI_API_KEY in your .env file.")

genai.configure(api_key=api_key)

# --- Model Setup ---
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Your Roast Prompt ---
prompt = """
Generate a short, brutal, and funny roast in Hinglish for a user who has been scrolling Instagram for 3 hours straight. The roast should be about their career goals.
"""

# --- Generate the Roast ---
try:
    response = model.generate_content(prompt)
    print("AI Generated Roast:")
    print("--------------------")
    print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")