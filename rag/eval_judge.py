from openai import OpenAI
from rag_engine import answer_question
from eval_dataset import EVAL_QUESTIONS

client = OpenAI()

def judge_answer(question, answer, context_sources):
    prompt = f"""You are evaluating an AI assistant's answer for quality.

Question: {question}
Answer given: {answer}
Sources used: {context_sources}

Rate the answer on a scale of 1-5 where:
1 = Completely wrong or hallucinated
3 = Partially correct but missing details
5 = Accurate, complete, well-grounded in sources

Respond with ONLY a number 1-5, nothing else."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        score = int(response.choices[0].message.content.strip())
    except ValueError:
        score = 0

    return score

def run_judge_eval():
    scores = []
    for q in EVAL_QUESTIONS:
        result = answer_question(q["question"])
        score = judge_answer(q["question"], result["answer"], result["sources"])
        scores.append(score)
        print(f"\nQ: {q['question']}")
        print(f"Score: {score}/5")

    avg = sum(scores) / len(scores)
    print(f"\nAverage score: {avg:.1f}/5")
    return avg

if __name__ == "__main__":
    run_judge_eval()