from openai import OpenAI
from vector_store import search, index_documents
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def answer_question(question, n_chunks=3):
    results = search(question, n_results=n_chunks)

    if not results:
        return "No relevant documents found."
    
    context = ""
    sources = []
    for chunk, source in results:
        context += f"\n--\n{chunk}"
        if source not in sources:
            sources.append(sources)
    prompt = f"""You are a helpful assistant that answers questions about the vAIbrant security scanner.

Use ONLY the following context to answer the question.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    return {
        "qestion": question,
        "answer": answer,
        "sources": sources,
        "chunks_used": len(results)
    }

if __name__ == "__main__":
    questions = [
        "How does vAIbrant authenticate API requests?",
        "What risk levels does vAIbrant use?",
        "What database does vAIbrant use to store results?",
        "What programming languages can vAIbrant analyze?",
        "What are the protocols in C++ added in the code?"
    ]

    for q in questions:
        print(f"\nQ: {q}")
        result = answer_question(q)
        print(f"A: {result['answer']}")
        print(f"Sources: {result['sources']}")