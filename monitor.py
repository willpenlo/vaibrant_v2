import time, json, datetime, os

MONITOR_LOG = "monitor_log.json"

def load_log():
    if os.path.exists(MONITOR_LOG):
        with open(MONITOR_LOG, "r") as f:
            return json.load(f)
    return []

def log_request(endpoint, input_tokens, output_tokens, latency_ms, success=True):
    log = load_log()
    cost = (input_tokens * 0.0000015) + (output_tokens * 0.0000006)
    log.append({
        "endpoint": endpoint,
        "timestamp": datetime.datetime.now().isoformat(),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "latency_ms": latency_ms,
        "cost_usd": round(cost, 6),
        "success": success
    })
    with open(MONITOR_LOG, "w") as f:
        json.dump(log, f, indent=2)

def get_stats_data():
    log = load_log()
    if not log:
        return "No data yet"
    total_cost = sum(e["cost_usd"] for e in log)
    avg_latencty = sum(e["latency_ms"] for e in log) / len(log)
    failed = sum(1 for e in log if not e["success"])
    return{
        "total_requests": len(log),
        "total_cost_usd": round(total_cost, 4),
        "avg_latency_ms": round(avg_latencty, 2),
        "failed_requests": failed,
        "success_rate": f"{(len(log) - failed)/len(log)*100:.1f}%"
    }

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, *args):
        self.elapsed_ms = (time.time() - self.start) * 1000

if __name__ == "__main__":
    log_request("analyze", 150, 300, 1200, success=True)
    log_request("analyze", 200, 400, 980, success=True)
    log_request("analyze", 100, 0, 500, success=False)
print(get_stats_data())