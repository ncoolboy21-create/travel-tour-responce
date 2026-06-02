import os
import json
import numpy as np
import requests
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from openai import AzureOpenAI

load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Azure client
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT
)


with open("travel_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

embeddings = np.load("travel_embeddings.npy")

print(f"Loaded {len(chunks)} chunks")
print(f"Embeddings shape: {embeddings.shape}")


EMBED_URL = "http://localhost:11434/api/embeddings"

def get_embedding(text):
    response = requests.post(
        EMBED_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        },
        timeout=60
    )
    response.raise_for_status()
    return np.array(response.json()["embedding"])


def search(query, top_k=5):
    query_emb = get_embedding(query).reshape(1, -1)

    scores = cosine_similarity(query_emb, embeddings)[0]
    top_indices = scores.argsort()[-top_k:][::-1]

    results = []
    for i in top_indices:
        results.append({
            "score": float(scores[i]),
            "text": chunks[i]
        })

    return results


def generate_answer(query):
    results = search(query)

    context = "\n\n".join([r["text"] for r in results])

    messages = [
        {
            "role": "system",
            "content": (
                "You are a travel planning assistant. "
                "Use ONLY the provided context. "
                "Recommend 2–3 best destinations."
            )
        },
        {
            "role": "user",
            "content": f"""
CONTEXT:
{context}

QUESTION:
{query}

Give a structured travel recommendation.
"""
        }
    ]

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("Type 'exit' to quit\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            break

        answer = generate_answer(query)

        print("\n Bot:\n")
        print(answer)
        print("\n" + "-" * 60 + "\n")