import ast

def parse_python_file(code):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"error": str(e)}
    
    result = {"imports": [], "functions": [], "classes": [], "dangerous_calls": []}
    dangerous = ["os.system", "subprocess", "eval", "exec"]

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)
        if isinstance(node, ast.ImportFrom):
            result["imports"].append(node.module)
        if isinstance(node, ast.FunctionDef):
            result["functions"].append(node.name)
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                val = getattr(node.func.value, "id", "")
                call = f"{val}.{node.func.attr}"
                if any(d in call for d in dangerous):
                    result["dangerous_calls"].append(call)
    return result

if __name__ == "__main__":
    with open("test_code.py", "r") as f:
        code = f.read()
    r = parse_python_file(code)
    print("Imports:", r["imports"])
    print("Functions:", r["functions"])
    print("Dangerous:", r["dangerous_calls"])