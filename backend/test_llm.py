import os
from dotenv import load_dotenv

# Load .env explicitly
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("No API key found in .env!")
    exit(1)

# Strip quotes if they exist
api_key = api_key.strip('"').strip("'")
os.environ["GEMINI_API_KEY"] = api_key

print("\n=== Testing LangChain LLM ===")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    models_to_test = [
        "gemini-1.5-flash", 
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro"
    ]
    
    success = False
    for model_name in models_to_test:
        print(f"Attempting to connect to {model_name}...")
        try:
            llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=api_key)
            response = llm.invoke("Hello, say SUCCESS")
            print(f"Success! Model {model_name} responded: {response.content}")
            success = True
            break
        except Exception as e:
            print(f"Failed with {model_name}: {e}\n")
            
    if not success:
        print("All models failed!")
except Exception as e:
    print(f"Outer Error: {e}")
