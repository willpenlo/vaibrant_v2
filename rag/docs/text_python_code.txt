import os 

from fastapi import FastAPI, HTTPException, UploadFile, File, Header
from pydantic import BaseModel
from scanner import SecurityScanner
from database import get_all_scans, get_scans_by_risk, get_scan_by_id
from typing import Optional

VAIBRANT_API_KEY = os.getenv("VAIBRANT_API_KEY")

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != VAIBRANT_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid or missing API key."
        )

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
    return {"message": "vAIbrant Security Scanner API is running.", "version": "1.0"}

@app.post("/analyze")
def analyze_code(request: CodeRequest,
                 x_api_key: Optional[str] = Header(None)):
    verify_api_key(x_api_key)
    
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    scanner = SecurityScanner()
    prompt = scanner.build_prompt(request.code, request.filename)
    analysis = scanner.call_api(prompt)
    risk = scanner.extract_risk_level(analysis)
    
    return AnalysisResponse(
        filename=request.filename,
        risk_level=risk,
        analysis=analysis
    )

@app.post("/analyze/upload")
async def analyze_file_upload(file: UploadFile = File(...),x_api_key: Optional[str] = Header(None)):
    verify_api_key(x_api_key)
    
    allowed = [".py", ".js", ".ts"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Only {allowed} files supported")
    
    contents = await file.read()
    
    if len(contents) > (50 * 1024):
        raise HTTPException(status_code=400, detail="File too large — max 50KB")
    
    try:
        code = contents.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
    
    if not code.strip():
        raise HTTPException(status_code=400, detail="File is empty")
    
    scanner = SecurityScanner()
    prompt = scanner.build_prompt(code, file.filename)
    analysis = scanner.call_api(prompt)
    risk = scanner.extract_risk_level(analysis)
    
    return {
        "filename": file.filename,
        "risk_level": risk,
        "lines_of_code": len(code.splitlines()),
        "analysis": analysis
    }

@app.get("/history")
def get_history(x_api_key: Optional[str] = Header(None)):
    verify_api_key(x_api_key)

    scans = get_all_scans()
    return {"total": len(scans), "scans": scans}

@app.get("/history/last/five")
def get_last_five_scans():
    all_scans = get_all_scans()
    return {"total": len(all_scans[:5]), "scans": all_scans[:5]}

@app.get("/history/{risk_level}")
def get_by_risk(risk_level: str):
    valid = ["LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"]
    level = risk_level.upper()
    if level not in valid:
        raise HTTPException(status_code=400, detail=f"Invalid risk. Choose from: {valid}")
    scans = get_scans_by_risk(level)
    return {"risk_level": level, "total": len(scans), "scans": scans}

@app.get("/stats")
def get_stats(x_api_key: Optional[str] = Header(None)):
    verify_api_key(x_api_key)

    all_scans = get_all_scans()
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
    for s in all_scans:
        lv = s["risk_level"]
        if lv in counts:
            counts[lv] += 1
    return {"total_scans": len(all_scans), "by_risk": counts}