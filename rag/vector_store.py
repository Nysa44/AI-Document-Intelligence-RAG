import os,pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH="data/index/index.faiss"
META_PATH="data/index/metadata.pkl"

class VectorStore:
    def __init__(self,model_name):
        self.encoder=SentenceTransformer(model_name)
        self.index=None
        self.metadata=[]
        self.load()

    @property
    def ready(self):
        return self.index is not None and bool(self.metadata)

    def create(self,metadata):
        self.metadata=metadata
        if not metadata:
            self.index=None
            return
        embeddings=self.encoder.encode(
            [x["text"] for x in metadata],
            normalize_embeddings=True,
            show_progress_bar=False
        )
        embeddings=np.asarray(embeddings,dtype="float32")
        self.index=faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        os.makedirs("data/index",exist_ok=True)
        faiss.write_index(self.index,INDEX_PATH)
        with open(META_PATH,"wb") as f:
            pickle.dump(metadata,f)

    def load(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            self.index=faiss.read_index(INDEX_PATH)
            with open(META_PATH,"rb") as f:
                self.metadata=pickle.load(f)

    def search(self,query,top_k=5):
        if not self.ready:
            return []
        emb=self.encoder.encode([query],normalize_embeddings=True,show_progress_bar=False)
        emb=np.asarray(emb,dtype="float32")
        scores,ids=self.index.search(emb,min(top_k,len(self.metadata)))
        result=[]
        for rank,idx in enumerate(ids[0]):
            if idx>=0:
                item=dict(self.metadata[idx])
                item["score"]=float(scores[0][rank])
                result.append(item)
        return result
