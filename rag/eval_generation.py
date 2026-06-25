from rag_engine import answer_question
from eval_dataset import EVAL_QUESTIONS

def check_answer(question_data):
    question = question_data["question"]
    expected_keywords = question_data["expected_keywords"]
    should_refuse = question_data.get("should_refuse", False)

    result = answer_question(question)
    answer_lower = result["answer"].lower()
 
    if should_refuse:
        refused = "don't have enough information" in answer_lower or "cannot" in answer_lower
        return {
            "question": question,
            "passed": refused,
            "answer": result["answer"]
        }
    
    keywords_found = [kw for kw in expected_keywords if kw.lower() in answer_lower]
    passed  = len(keywords_found) >= len(expected_keywords)*0.5

    return {
        "question": question,
        "passed": passed,
        "keywords_found": keywords_found,
        "expected_keywords": expected_keywords,
        "answer": result["answer"]
    }

def run_generation_eval():
    results =[]
    for q in EVAL_QUESTIONS:
        result = check_answer(q)
        results.append(result)

    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    print(f"\nGeneration Eval Results: {passed}/{total} passed\n")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['question']}")
        if not r["passed"]:
            print(f" Answer: {r['answer'][:150]}")
    return passed, total

if __name__ == "__main__":
    run_generation_eval()