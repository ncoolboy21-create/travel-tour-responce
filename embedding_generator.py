import json
import requests
import numpy as np

OLLAMA_URL = "http://localhost:11434/api/embeddings"

def get_embedding(text):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    response.raise_for_status()

    return response.json()["embedding"]

# Load chunks
with open(r"C:\Users\shlok\Desktop\GenAI\GenAIProject\rag_model\travel_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

all_embeddings = []

for i, chunk in enumerate(chunks):
    print(f"Embedding {i+1}/{len(chunks)}")

    embedding = get_embedding(chunk)

    all_embeddings.append(embedding)

embeddings = np.array(all_embeddings, dtype=np.float32)

print("Embedding shape:", embeddings.shape)

np.save(r"C:\Users\shlok\Desktop\GenAI\GenAIProject\rag_model\travel_embeddings.npy", embeddings)

print("Embeddings saved successfully!")