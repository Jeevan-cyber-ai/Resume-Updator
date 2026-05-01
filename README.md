# 🧠 Smart Resume Tailor AI

An AI-powered web application that automatically analyzes your resume, compares it against a specific Job Description (JD), identifies skill gaps, and rewrites it to be perfectly tailored for that role — all while staying 100% truthful.

---

## 🎯 What It Does

Upload your existing resume. Paste a Job Description. Let the AI do the heavy lifting.

| Step | Action |
|------|--------|
| 1 | Upload resume (PDF or DOCX) |
| 2 | AI extracts all resume data into structured JSON |
| 3 | User pastes the target Job Description |
| 4 | AI compares resume vs JD |
| 5 | Detects missing skills and weak sections |
| 6 | Interactively asks user for missing details |
| 7 | Rewrites and customizes resume for that specific job |
| 8 | Generates downloadable DOCX, PDF, and HTML outputs |

---

## 💡 Problem Solved

Job seekers manually rewrite their resume for every application. This is tedious and error-prone.

**Example:**
- You have a Web Developer resume
- You're now applying for a Data Analyst role
- You need to rewrite your summary, reorder skills, update project highlights, and add ATS keywords

**Smart Resume Tailor AI automates this entire process.**

---

## ⚠️ Ethics First

This tool **never** fakes your experience. It only:
- Improves the wording of what you already have
- Highlights relevant existing skills
- Asks you about missing details
- Suggests areas to learn and grow

---

## 🏗️ Project Structure

```
smart-resume-ai/
│
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # API keys (not committed to git)
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── resume.py              # API routes for resume upload & processing
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py              # PDF and DOCX text + hyperlink extraction
│   │   ├── extractor.py           # LangChain + Gemini structured extraction
│   │   └── direct_extractor.py   # Direct file-to-Gemini extraction (multimodal)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── resume.py              # Pydantic schema for structured resume data
│   │
│   ├── uploads/                   # Uploaded resume files (temp storage)
│   ├── test_llm.py               # Test script to verify LLM connectivity
│   └── test_direct.py            # Test script for direct file extraction
│
├── run_backend.bat                # One-click backend startup (Windows)
└── README.md
```

---

## 🔥 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI + Uvicorn |
| AI Model | Google Gemini 2.5 Flash |
| AI Framework | LangChain + google-genai |
| PDF Parsing | PyMuPDF (fitz) |
| DOCX Parsing | python-docx |
| Data Validation | Pydantic |
| Environment | python-dotenv |
| Frontend *(Upcoming)* | React.js + Tailwind CSS |
| Database *(Upcoming)* | SQLite → PostgreSQL |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A **Google Gemini API key** from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd smart-resume-ai
```

### 2. Set Up Virtual Environment
```bash
cd backend
python -m venv venv

# Windows (PowerShell)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key
Open `backend/.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```
> ⚠️ Do not use quotes around the key.

### 5. Run the Backend
```bash
# Option A: Using the bat script (Windows)
run_backend.bat

# Option B: Manual
cd backend
uvicorn main:app --reload
```

The API will be live at: **http://127.0.0.1:8000**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/api/upload-resume` | Upload + text-based AI extraction |
| `POST` | `/api/upload-resume-llm` | Upload + direct multimodal Gemini extraction *(recommended)* |

### Interactive API Docs
Once the server is running, visit: **http://127.0.0.1:8000/docs**

---

## 📋 Extracted Resume Schema

The AI extracts your resume into this structured JSON:

```json
{
  "name": "Alice Smith",
  "email": "alice@example.com",
  "phone": "+91 98765 43210",
  "location": "Chennai, India",
  "linkedin": "https://linkedin.com/in/alice-smith",
  "github": "https://github.com/alicesmith",
  "objectives": "Data Scientist with 3 years experience...",
  "skills": ["Python", "SQL", "Machine Learning"],
  "projects": [
    { "name": "Sales Dashboard", "description": "Built using Tableau and SQL..." }
  ],
  "education": [
    { "degree": "B.E. Computer Science", "institution": "Anna University", "year": "2022" }
  ],
  "experience": [
    { "role": "Data Analyst", "company": "TechCorp", "duration": "2022–2024", "description": "..." }
  ],
  "certifications": ["Google Data Analytics", "AWS Cloud Practitioner"]
}
```

---

## 🧪 Testing

Test your LLM connection before starting the server:

```bash
# Verify Gemini API connectivity
python test_llm.py

# Test direct file-to-LLM extraction
python test_direct.py
```

---

## 📌 Current Status (MVP Phase 1 Complete)

- [x] Resume upload (PDF and DOCX)
- [x] Text extraction with hidden hyperlink detection (LinkedIn, GitHub URLs)
- [x] AI-powered structured data extraction (Gemini 2.5 Flash)
- [x] Dual extraction strategy: text-based and direct multimodal
- [ ] Job Description Analyzer *(coming next)*
- [ ] Resume vs JD Comparison *(coming next)*
- [ ] Interactive Q&A for missing details (LangGraph)
- [ ] Tailored Resume Rewriter
- [ ] DOCX / PDF / HTML output generator
- [ ] React Frontend

---

## 🔮 Future Roadmap

- 📝 Cover Letter Generator
- 💼 LinkedIn Profile Optimizer
- 📊 ATS Score Dashboard
- 🤖 AI Mock Interview Questions
- 🎨 Canva-ready Export
- 🔗 GitHub & LeetCode Profile Import

---

## 📄 License

This project is for educational and personal use. Not intended for misrepresentation of qualifications.
