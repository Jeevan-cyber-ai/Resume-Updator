@echo off
echo Starting the FastAPI backend...
cd backend
uvicorn main:app --reload
pause
