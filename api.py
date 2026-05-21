from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from scanner import SecurityScanner
from database import get_all_scans, get_scans_by_risk, get_scan_by_id


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

@app.get("/history")
def get_history():
    scans = get_all_scans()
    return {"total": len(scans), "scans": scans}

@app.get("/history/{risk_level}")
def get_by_risk(risk_level: str):
    valid = ["LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"]
    level = risk_level.upper()
    if level not in valid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid risk. Choose from: {valid}"
        )
    scans = get_scans_by_risk(level)
    return {"risk_level": level, "total": len(scans), "scans": scans}

@app.get("/stats")
def get_stats():
    all_scans = get_all_scans()
    counts = {"CRITICAL": 0, "HIGH":0, "MEDIUM":0, "LOW":0, "UNKNOWN":0}
    for s in all_scans:
        lv = s["risk_level"]
        if lv in counts:
            counts[lv] += 1
    return {"total_scans": len(all_scans), "risk_counts": counts}

@app.get("/history/last/five")
def get_last_five_scans():
    all_scans = get_all_scans()
    last_five = all_scans[:5]
    return {"total": len(last_five), "scans": last_five}

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