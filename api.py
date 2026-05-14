from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from scanner import SecurityScanner

app = FastAPI(title="vAIbrant Security Scanner API!", version="1.0")

class CodeRequest(BaseModel):
    code: str
    filename: str = "unknown.py"

class AnalysisResponse(BaseModel):
    filename: str
    risk_level: str
    analysis: str

@app.get("/")
def root():
    return{"message": "vAIbrant Security Scanner API is running.", "version": "1.0"}

@app.post("/analyze")
async def analyze_file_upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".py"):
        raise HTTPException(
            status=400,
            detail="Only .py files are supported."
        )
    
    contents = await file.read()

    try:
        code = contents.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status=400,
            detail="File must be a valid UTF-8 encoded text file."
        )
    
    if not code.strip():
        raise HTTPException(
            status=400,
            detail="File is empty."
        )
    
    if len(contents) > (50 * 1024):  # Limit to 50 KB
        raise HTTPException(
            status=400,
            detail="File size exceeds the 50 KB limit."
        )
    
    scanner = SecurityScanner()
    prompt = scanner.build_prompt(code, file.filename)
    analysis = scanner.call_api(prompt)
    risk = scanner.extract_risk_level(analysis)

    return{
        "filename": file.filename,
        "risk_level": risk,
        "lines_of_code": len(code.splitlines()),
        "analysis": analysis
    }