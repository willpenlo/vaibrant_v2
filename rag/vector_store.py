import chromadb
from embedder import chunk_text, embed_text, load_documents

client = chromadb.PersistentClient(path="./chroma_db")

def get_collection():
    return client.get_or_create_collection(
        name="vaibrant_docs",
        metadata={"hnsw:space": "cosine"}
    )

def index_documents(docs_folder="docs"):
    collection = get_collection()
    docs = load_documents(docs_folder)

    total_chunks = 0
    for doc in docs:
        chunks = chunk_text(doc["content"])
        for i, chunk in enumerate(chunks):
            embedding = embed_text(chunk)
            chunk_id = "{doc['filepath']}_{i}"
            collection.upsert(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": doc["filepath"], "chunk_index": i}]
            )
            total_chunks += 1

def search(query, n_results=3):
    collection = get_collection()
    query_embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    chunks = results["documents"][0]
    sources = [m["source"] for m in results ["metadatas"][0]]
    return list(zip(chunks, sources))

if __name__ == "__main__":
    index_documents()
    print("\nTesting search...")
    results = search("how does the scanner work?")
    for chunk, source in results:
        print(f"\nSource: {source}")
        print(f"Chunk: {chunk[:200]}...")