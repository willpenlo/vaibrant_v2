from logging import log
import os, json, datetime

PROMPTS_DIR = "prompts"
PROMPT_LOG = "prompt_log.json"

def load_prompt(version="v1"):
    path = os.path.join(PROMPTS_DIR, f"SECURITY_ANALYSIS_{version}.txt")
    with open(path, "r") as f:
              return f.read()

def render_prompt(version="v1", **kwargs):
       return load_prompt(version).format(**kwargs)

def log_prompt_use(version, input_tokens=0, output_tokens=0):
    log = []
    if os.path.exists(PROMPT_LOG):
        with open(PROMPT_LOG, "r") as f:
            log = json.load(f)
    log.append({
        "version": version,
        "used_at": datetime.datetime.now().isoformat(),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    })
    with open(PROMPT_LOG, "w") as f:
        json.dump(log, f, indent=2)

def get_prompt_stats():
    if not os.path.exists(PROMPT_LOG):
        return {}
    with open(PROMPT_LOG, "r") as f:
        log = json.load(f)
    stats = {}
    for e in log:
        v = e["version"]
        if v not in stats:
            stats[v] = {
                "uses": 0,
                "total_tokens": 0
            }
        stats[v]["uses"] += 1
        stats[v]["total_tokens"] += e.get("input_tokens", 0) + e.get("output_tokens", 0)
    return stats

if __name__ == "__main__":
    p = render_prompt(
        "v1",
        filename="test.py",
        imports=["os"],
        functions=["run"],
        dangerous_calls=["os.system"],
        code="import os\nos.system('rm -rf /')"
        )
    print(p)
    log_prompt_use("v1", 150, 300)
    print(get_prompt_stats())
    
             