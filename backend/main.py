# backend/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
from routes.resume import router as resume_router
from routes.improve import router as improve_router

# Load env variables before importing routes that might use them
load_dotenv()

app = FastAPI(
    title="Smart Resume Tailor AI API",
    description="API for parsing and analyzing resumes",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to specific frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router, prefix="/api", tags=["Resume"])
app.include_router(improve_router, prefix="/api", tags=["Improve"])

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Resume Tailor AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
