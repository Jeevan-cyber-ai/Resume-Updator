import os
import json
import time
from google import genai
from services.parser import extract_text_from_docx
from prompts.extract import DIRECT_EXTRACT_PROMPT
from services.parser import extract_text_from_pdf
def extract_from_file_directly(file_path: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY is not set."}
        
    api_key = api_key.strip('"').strip("'")
    
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = DIRECT_EXTRACT_PROMPT
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            print(f"Uploading {file_path} to Gemini...")
            uploaded_file = client.files.upload(file=file_path)
            
            # Extract links from PDF so Gemini can see hidden URLs
            
            extracted_text = extract_text_from_pdf(file_path)
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[uploaded_file, f"Here is the text and any extracted URLs for context:\n{extracted_text}\n\n", prompt]
            )
            
            try:
                client.files.delete(name=uploaded_file.name)
            except Exception as e:
                print(f"Cleanup error (safe to ignore): {e}")
                
        elif ext in [".docx", ".doc"]:
            print(f"Extracting text locally from {file_path} since Gemini doesn't natively support DOCX...")
            text_content = extract_text_from_docx(file_path)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[f"Resume Text:\n{text_content}\n\n", prompt]
            )
        else:
            return {"error": f"Unsupported file type: {ext}"}
            
        result_text = response.text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        elif result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
            
        return json.loads(result_text.strip())
        
    except json.JSONDecodeError as e:
        print("Failed to parse JSON response")
        return {"error": "Model did not return valid JSON."}
    except Exception as e:
        print(f"Error in direct LLM extraction: {e}")
        return {"error": str(e)}
