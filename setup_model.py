import os
from sentence_transformers import SentenceTransformer

name=os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
print("Loading:", name)
SentenceTransformer(name)
print("Embedding model ready.")
