from eval_retrieval import run_retrieval_eval
from eval_generation import run_generation_eval
from eval_judge import run_judge_eval

print("=" * 50)
print("RUNNING FULL EVAL SUITE")
print("=" * 50)

r_passed, r_total = run_retrieval_eval()
g_passed, g_total = run_generation_eval()
avg_score = run_judge_eval()

print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print(f"Retrieval: {r_passed}/{r_total}")
print(f"Generation: {g_passed}/{g_total}")
print(f"LLM Judge avg: {avg_score:.1f}/5")