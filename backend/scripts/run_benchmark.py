import sys, json
from sentence_transformers import SentenceTransformer
import faiss

# Inputs
file_path, chunking, embedding_model, retriever = sys.argv[1:5]

# Load text
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Simple chunking
if chunking == "Fixed Size":
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
elif chunking == "Sliding Window":
    chunks = [text[i:i+300] for i in range(0, len(text), 200)]
else:
    chunks = [text]  # fallback: whole text

# Embedding model
if embedding_model == "LegalBERT":
    model = SentenceTransformer("nlpaueb/legal-bert-base-uncased")
else:
    model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Simulate retrieval (use fixed query for demo)
query = "What is the legal issue?"
query_emb = model.encode([query])
D, I = index.search(query_emb, k=3)

results = [chunks[i] for i in I[0]]

# Return JSON
print(json.dumps({
    "query": query,
    "results": results
}))
