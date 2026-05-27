from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import shutil
from .utils import extract_text_from_pdf, extract_text_from_docx, clean_text
from .model import AdvancedAnalyzer

app = FastAPI(title="Production-Grade Resume AI")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = AdvancedAnalyzer()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file format. Only PDF and DOCX are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract text
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_docx(file_path)
    
    clean_txt = clean_text(text)
    
    return {"filename": file.filename, "extracted_text": clean_txt[:1000] + "..."} # Return snippet for confirmation

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(None),
    job_role: str = Form("software_engineer"),
    custom_role: str = Form(None)
):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file format.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract text
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_docx(file_path)
    
    result = analyzer.analyze_advanced(text, job_role, custom_role, job_description)
    
    return result

from pydantic import BaseModel
from typing import Dict, Any

class ChatRequest(BaseModel):
    message: str
    context: Dict[str, Any]

@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    # Pass the message and context to our model's chat logic
    reply = analyzer.generate_chat_response(request.message, request.context)
    return {"reply": reply}

# Mount frontend static files at the end to avoid overriding API routes
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
