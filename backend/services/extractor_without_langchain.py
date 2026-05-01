# backend/services/extractor_without_langchain.py
import os
import json
from google import genai
from services.parser import extract_text
from prompts.extract import DIRECT_EXTRACT_PROMPT

def extract_resume_data_vanilla(file_path: str) -> dict:
    """
    Vanilla Python flow WITHOUT LangChain:
    1. Extracts text from the document.
    2. Manually calls the Gemini API.
    3. Manually cleans and parses the JSON string.
    
    COMPARE THIS TO extractor.py TO SEE WHAT LANGCHAIN DOES FOR YOU!
    """
    # 1. Parse Document (Same as LangChain flow)
    text = extract_text(file_path)
    if not text.strip():
        return {"error": "Could not extract text from document."}
        
    # 2. Setup API
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY is not set."}

    # 3. Initialize Native Client (No LangChain ChatGoogleGenerativeAI)
    client = genai.Client(api_key=api_key)
    
    # 4. Manually construct the prompt by adding the text
    # (No LangChain PromptTemplate)
    full_prompt = f"{DIRECT_EXTRACT_PROMPT}\n\nResume Text:\n{text}"
    
    try:
        print("Running vanilla extraction pipeline (No LangChain)...")
        
        # 5. Make the API Call manually
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        
        # 6. Manually clean markdown formatting and parse JSON 
        # (No LangChain JsonOutputParser)
        result_text = response.text.strip()
        
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        elif result_text.startswith("```"):
            result_text = result_text[3:]
            
        if result_text.endswith("```"):
            result_text = result_text[:-3]
            
        result_json = json.loads(result_text.strip())
        return result_json
        
    except json.JSONDecodeError:
        print("Failed to parse JSON response")
        return {"error": "Model did not return valid JSON."}
    except Exception as e:
        print(f"Error extracting data with AI: {e}")
        return {"error": str(e)}
