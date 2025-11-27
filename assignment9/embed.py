import google.generativeai as genai
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


phrases = [
    "The cat is sleeping",
    "A dog is running",
    "Quantum physics studies matter and energy"
]

print("Simple Embeddings")

simple_embeddings = []

for p in phrases:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=p
    )
    emb = result["embedding"]
    simple_embeddings.append(emb)
    print(f"Phrase: {p}\nVector length: {len(emb)}\n")


sim_matrix = cosine_similarity(simple_embeddings)
print("Cosine Similarity Matrix:")
print(sim_matrix)



data = {
    "title": ["Article 1", "Article 2"],
    "text": [
        "Quantum physics explores how particles behave at microscopic scales. "
        "It studies probability, waves, and the uncertainty principle.",

        "Machine learning is a field of artificial intelligence. "
        "It allows computers to learn patterns from data without explicit programming."
    ]
}

df = pd.DataFrame(data)


def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


df["chunks"] = df["text"].apply(chunk_text)


all_chunks = []
article_ids = []

for idx, row in df.iterrows():
    for chunk in row["chunks"]:
        all_chunks.append(chunk)
        article_ids.append(row["title"])

print("\n Total chunks created:", len(all_chunks), " ===")


chunk_embeddings = []

print("\n Generating embeddings for chunks ")

for c in all_chunks:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=c
    )
    chunk_embeddings.append(result["embedding"])


output = pd.DataFrame({
    "article": article_ids,
    "chunk": all_chunks,
    "embedding": chunk_embeddings
})

output.to_pickle("article_embeddings.pkl")


