import glob
import os
import sys
import datetime
import json
from openai import OpenAI
from dotenv import load_dotenv
from database import init_db, save_scan
from parser import parse_python_file

load_dotenv()

class SecurityScanner:

    def __init__(self):
        self.client = OpenAI()
        self.results = []
        self.skipped_files = []
        init_db()
    
    def read_file(self, filepath):
        try:
            with open(filepath, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: {filepath} not found.")
            self.skipped_files.append(filepath)
            return None
    def extract_risk_level(self, analysis):
        analysis_upper = analysis.upper()
        for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if level in analysis_upper:
                return level
        return "UNKNOWN"
    
    def build_prompt(self, code_content, filename):
        ext = filename.split(".")[-1] if "." in filename else "unknown"

        if ext == "py":
            from parser import parse_python_file
            structure = parse_python_file(code_content)
            pre = f"""Pre-analysis detected:
            - Imports: {structure.get('imports', [])}
            - Functions: {structure.get('functions', [])}
            - Dangerous calls: {structure.get('dangerous_calls', [])}"""
        else:
            pre = f"Language: {ext} (static analysis not available)"

        return f"""You are a security analyst for vAIbrant.

        File: {filename}
        {pre}

        Full code:
        {code_content}

        Analyze for:
        1. Security vulnerabilities
        2. Hardcoded secrets
        3. Dangerous function calls
        4. Risk level: LOW / MEDIUM / HIGH / CRITICAL
        
        At the end, format your response with clear sections. Add a section called non-technical language where you explain 
        the vulnerabilities in simple terms for non-technical users. 
        Remember to explain vulnerabilities in simple terms for non-technical users, and the potential impact if not addressed, 
        use simple terms and a professional tone, as if explaining to a business person.
        """
    
    def call_api(self, prompt):
        message = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return message.choices[0].message.content
    
    def save_report(self, filepath, analysis):
        time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = filepath.replace("/", "_").replace(".", "_")
        report_name = f"report_{base_name}_{time_stamp}.txt"

        with open(report_name, "w") as f:
            f.write(f"vAIbrant Security Report\n")
            f.write(f"File: {filepath}\n")
            f.write(f"Date: {datetime.datetime.now()}\n")
            f.write("=" * 50 + "\n\n")
            f.write(analysis)
        return report_name
    

    def analyze_file(self, filepath):
        print(f"\nAnalyzing: {filepath}")
        code = self.read_file(filepath)
        if code is None:
            return
        prompt = self.build_prompt(code, filepath)
        result = self.call_api(prompt)
        risk = self.extract_risk_level(result)
        structure = parse_python_file(code)
        scan_id = save_scan(
            filename=filepath,
            risk_level=risk,
            lines_of_code=len(code.splitlines()),
            analysis=result,
            imports=structure.get("imports", []),
            dangerous_calls=structure.get("dangerous_calls", [])
        )
        print(f"Saved to DB - ID: {scan_id}")
        report_name = self.save_report(filepath, result)
        self.results.append({
            "file": filepath,
            "risk": risk,
            "report": report_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "lines_of_code": len(code.splitlines())
        })
        print(f"Risk: {risk}")
        print(f"API RESPONSE: {result[:200]}")

    def scan_directory(self, directory):
        py_files = glob.glob(f"{directory}/**/*.py", recursive=True)
        print(f"Found {len(py_files)} files \n")
        for f in py_files:
            self.analyze_file(f)
        self.print_summary()
    
    def export_json(self, output_file="scan_results.json"):
        data = {
            "scan_date": datetime.datetime.now().isoformat(),
            "total_files": len(self.results),
            "results": self.results,
            "skipped_files": self.skipped_files
        }
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nJSON report saved to {output_file}")

    def print_summary(self):
        print("\n== SCAN SUMMARY ===")
        counts = {"CRITICAL":0, "HIGH":0, "MEDIUM":0, "LOW":0, "UNKNOWN":0}
        for r in self.results:
            counts[r["risk"]] += 1
            print(f"{r['risk']:10} - {r['file']}")
        print("\n--- Totals ---")
        for level, count in counts.items():
            if count > 0:
                print(f"{level}: {count}")
        self.export_json()


if __name__ == "__main__":
    scanner = SecurityScanner()
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if os.path.isdir(target):
            scanner.scan_directory(target)
        else:
            scanner.analyze_file(target)
    else:
        scanner.analyze_file("test_code.py")
        