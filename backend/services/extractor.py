# backend/services/extractor.py
import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from models.resume import ResumeSchema
from services.parser import extract_text

def extract_resume_data(file_path: str) -> dict:
    """
    Unified LangChain flow:
    1. Extracts text and hidden URLs from the document (PDF/DOCX).
    2. Uses LangChain PromptTemplate + JsonOutputParser.
    3. Runs the text through Gemini via LangChain.
    """
    # 1. Parse Document
    text = extract_text(file_path)
    if not text.strip():
        return {"error": "Could not extract text from document."}
        
    # 2. Setup API
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY is not set in environment variables."}

    # 3. Define LangChain LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, google_api_key=api_key)
    
    # 4. Define Output Parser using the Pydantic Schema
    parser = JsonOutputParser(pydantic_object=ResumeSchema)
    
    # 5. Define Prompt
    prompt = PromptTemplate(
        template="Extract the resume details from the following text and format it as valid JSON.\n\n{format_instructions}\n\nResume Text:\n{text}\n",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    # 6. Build and Invoke Chain
    chain = prompt | llm | parser
    
    try:
        print("Running LangChain extraction pipeline...")
        result = chain.invoke({"text": text})
        return result
    except Exception as e:
        print(f"Error extracting data with AI: {e}")
        return {"error": str(e)}
