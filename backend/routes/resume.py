# backend/routes/resume.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import uuid
from services.extractor import extract_resume_data
from models.compare import CompareRequest
from services.comparator import compare_resume_with_job

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
        
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
        
    # AI Extraction using the unified LangChain flow
    structured_data = extract_resume_data(file_path)
    
    if "error" in structured_data:
        raise HTTPException(status_code=500, detail=structured_data["error"])
        
    return {
        "filename": file.filename,
        "message": "Resume processed successfully via LangChain",
        "data": structured_data
    }


@router.post("/compare")
async def compare_resume(req: CompareRequest):
    if not req.job_title.strip():
        raise HTTPException(status_code=400, detail="job_title is required.")
    if not req.resume_data:
        raise HTTPException(status_code=400, detail="resume_data is required.")

    scores = compare_resume_with_job(req.resume_data, req.job_title)

    if "error" in scores:
        raise HTTPException(status_code=500, detail=scores["error"])

    return {
        "message": "Comparison complete",
        "job_title": req.job_title,
        "scores": scores
    }
