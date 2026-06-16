import os 
import glob
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def load_documents(docs_folder):
    documents = []
    txt_files = glob.glob(f"{docs_folder}/**/*.txt", recursive=True)
    py_files = glob.glob(f"{docs_folder}/**/*.py", recursive=True)

    for filepath in txt_files + py_files:
        with open(filepath, "r") as f:
            content = f.read()
        documents.append({
            "filepath": filepath,
            "content": content
        })
    return documents

if __name__=="__main__":
    docs = load_documents("docs")
    print(f"Loaded{len(docs)} documents")
    for doc in docs:
        chunks = chunk_text(doc["content"])
        print(f"Loaded {len(docs)} documents")
        if chunks:
            embedding = embed_text(chunks[0])
            print(f"First chunk embedding lenght: {len(embedding)}")
            