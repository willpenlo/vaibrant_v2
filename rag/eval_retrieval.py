from vector_store import search
from eval_dataset import EVAL_QUESTIONS

def check_retrieval(question_data):
    question = question_data["question"]
    expected_source = question_data["expected_source"]

    results = search(question, n_results=3)
    retrieved_sources = [source for _, source in results]

    if expected_source is None:
        return{
            "question": question,
            "passed": True,
            "note": "No expected source (refusal case)"
        }
    
    found = any(expected_source in s for s in retrieved_sources)

    return {
        "question": question,
        "expected_source": expected_source,
        "retrieved_sources": retrieved_sources,
        "passed": found
    }

def run_retrieval_eval():
    results = []
    for q in EVAL_QUESTIONS:
        result = check_retrieval(q)
        results.append(result)
    
    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    print(f"\nRetrieval Eval Results: {passed}/{total} passed\n")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['question']}")
        if not r["passed"]:
            print(f" Expected: {r.get('expected_source')}")
            print(f" Got: {r.get('retrieved_sources')}")
    return passed, total

if __name__ == "__main__":
    run_retrieval_eval()

