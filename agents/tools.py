import datetime
import os
import glob
import sys

sys.path.append("../")

from scanner import SecurityScanner

def scan_file_for_security(filepath):
    """Scans a Python or JS file for security vulnerabilities using vAIbrant."""

    try:
        with open(filepath, "r") as f:
            code = f.read()
    except FileNotFoundError:
        return f"Error: File {filepath} not found"
    
    scanner = SecurityScanner()
    prompt = scanner.build_prompt(code, filepath)
    analysis = scanner.call_api(prompt)
    risk = scanner.extract_risk_level(analysis)

    return f"Risk level: {risk}\n\nAnalysis:\n{analysis[:500]}"

def get_current_time():
    """Returns the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def list_python_files(directory="."):
    """Lists all Python files in a directory."""
    files = glob.glob(f"{directory}/**/*.py", recursive=True)
    return files if files else ["No Python files found"]

def read_file(filepath):
    """Reads and returns the contents of a file."""
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File {filepath} not found"
    except Exception as e:
        return f"Error: {e}"

def count_lines(filepath):
    """Counts the number of lines in a file."""
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
        return f"{filepath} has {len(lines)} lines"
    except FileNotFoundError:
        return f"Error: File {filepath} not found"

def summarize_scan_history():
    """Returns a summary of recent scans from the vAIbrant db"""
    sys.path.append("../")

    from database import get_all_scans

    scans = get_all_scans()
    if not scans:
        return "No scans found in the database."
    
    summary = f"Total scans: {len(scans)}\n"
    for scan in scans[:5]:
        summary += f"- {scan['filename']}: {scan['risk_level']}, {scan["scanned_at"]}\n"
    return summary

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current date and time",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_python_files",
            "description": "Lists all Python files in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Directory to search in"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_lines",
            "description": "Counts the number of lines in a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scan_file_for_security",
            "description": "Scans a Python or JS file for security vulnerabilties.",
            "parameters":{
                "type": "object",
                "properties":{
                    "filepath": {
                        "type": "string",
                        "description": "Path to file to scan"
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "summarize_scan_history",
        "description": "Returns a summary of recent security scans from the database",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }
}
]

TOOL_MAP = {
    "get_current_time": get_current_time,
    "list_python_files": list_python_files,
    "read_file": read_file,
    "count_lines": count_lines,
    "scan_file_for_security": scan_file_for_security,
    "summarize_scan_history": summarize_scan_history
}