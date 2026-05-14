import os
import sys
import datetime
import openai
import glob
from dotenv import load_dotenv

load_dotenv()

def read_file(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"Error readingn file {e}")
        return None

def build_prompt(code_content, filename):
    return f"""
    You are a security analys reviewing code for the vaibrant tool.

    File: {filename}

Analyze for:
1. Security vulnerabilities (SQL injection, command injection, etc.)
2. Hardcoded secrets or credentials
3. Dangerous function calls
4. Overall risk: LOW / MEDIUM / HIGH / CRITICAL

Code:
{code_content}

Format your response with clear sections.

Add a section called non-technical language where you explain th vulnerabilities in simple terms for non-technical users, 
in a much simpler language and explain what could go wrong if the vulnerabilities are not taken care of, 
and how it could impact the users. Use a professional tone and make sure you explain as if you were explaining to a business person. 
"""

def call_openai(prompt):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

def analyze_file(filepath):
    print(f"\nAnalyzing: {filepath}")
    print("=" * 50)

    code = read_file(filepath)
    if code is None:
        return ""
    
    prompt = build_prompt(code, filepath)
    result = call_openai(prompt)

    print(result)

    risk = extract_risk_level(result)
    report_name = save_report(filepath, result)
    
    print(f"\nRisk level detected: {risk}")
    print(f"Report saved to: {report_name}")
    print("-" * 50)

    return result

def save_report(filepath, analysis):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = filepath.replace("/", "_").replace(".", "_")
    report_name = f"report_{base_name}_{timestamp}.txt"

    with open(report_name, "w") as f:
        f.write(f"vAIbrant Security Report\n")
        f.write(f"File analyzed: {filepath}\n")
        f.write(f"Date: {datetime.datetime.now()}\n")
        f.write(analysis)

    return report_name

def print_summary(results):
    print("\n"+"="*50)
    print("SCAN SUMMARY")
    print("="*50)

    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}

    for r in results:
        risk = r["risk"]
        counts[risk] = counts[risk] + 1
        print(f"{risk:10} = {r['file']}")

    print("\n--- Totals ---")
    for level, count in counts.items():
        if count > 0:
            print(f"{level}: {count} file(s)")


def extract_risk_level(analysis):
    analysis_upper = analysis.upper()
    for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if level in analysis_upper:
            return level
    return "UNKNOWN"

def scan_directory(directory):
    py_files = glob.glob(f"{directory}/**/*.py", recursive=True)

    if len(py_files) == 0:
        print(f"No Python files found in {directory}")
        return
    
    print("Found {len(py_files)} Python files \n")

    results = []

    for filepath in py_files:
        analysis = analyze_file(filepath)
        risk = extract_risk_level(analysis)
        results.append({
            "file": filepath,
            "risk": risk
        })
    
    print_summary(results)



def main():
    if len(sys.argv)>1:
        target = sys.argv[1]
        if os.path.isdir(target):
            scan_directory(target)
        else:
            analyze_file(target)

    else:
        analyze_file("test_code.py")

main()