import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("No API key found in .env!")
    exit(1)

api_key = api_key.strip('"').strip("'")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print("Fetching available models from Google API...")
try:
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json().get('models', [])
        valid_models = [m['name'] for m in models if 'generateContent' in m.get('supportedGenerationMethods', [])]
        print("\n=== Models available for Generate Content ===")
        for name in valid_models:
            print(f"- {name.replace('models/', '')}")
    else:
        print(f"Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"Failed to fetch models: {e}")
