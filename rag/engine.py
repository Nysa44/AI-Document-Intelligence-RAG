import os
from pathlib import Path
from .chunker import chunk_text
from .document_loader import is_supported,load_document
from .generator import AnswerGenerator
from .vector_store import VectorStore

class RAGEngine:
    def __init__(self):
        self.embedding_model=os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
        self.top_k=int(os.getenv("TOP_K","5"))
        self.chunk_size=int(os.getenv("CHUNK_SIZE","850"))
        self.chunk_overlap=int(os.getenv("CHUNK_OVERLAP","120"))
        self.store=VectorStore(self.embedding_model)
        self.generator=AnswerGenerator()

    @property
    def index_ready(self):
        return self.store.ready

    @property
    def llm_configured(self):
        return self.generator.configured

    def build_index(self):
        folder=Path("data/uploads")
        folder.mkdir(parents=True,exist_ok=True)
        metadata=[]
        for path in sorted(folder.iterdir()):
            if not path.is_file() or not is_supported(path.name):
                continue
            try:
                for page_data in load_document(path):
                    for cid,text in enumerate(chunk_text(page_data["text"],self.chunk_size,self.chunk_overlap)):
                        metadata.append({
                            "source":path.name,
                            "chunk_id":cid,
                            "page":page_data.get("page"),
                            "text":text
                        })
            except Exception as exc:
                print("Skipped",path.name,exc)
        self.store.create(metadata)

    def ingest_files(self,files):
        accepted=0
        rejected=[]
        folder=Path("data/uploads")
        folder.mkdir(parents=True,exist_ok=True)
        for file in files:
            name=Path(file.filename or "").name
            if not name:
                continue
            if not is_supported(name):
                rejected.append({"file":name,"reason":"Unsupported file type"})
                continue
            file.save(folder/name)
            accepted+=1
        self.build_index()
        return {"accepted":accepted,"rejected":rejected,"stats":self.stats()}

    def ask(self,question):
        contexts=self.store.search(question,self.top_k)
        return {
            "answer":self.generator.generate(question,contexts),
            "sources":[
                {
                    "source":x["source"],
                    "chunk_id":x["chunk_id"],
                    "page":x.get("page"),
                    "score":round(x["score"],4),
                    "preview":x["text"][:300]
                } for x in contexts
            ]
        }

    def stats(self):
        return {
            "documents":len({x["source"] for x in self.store.metadata}),
            "chunks":len(self.store.metadata),
            "index_ready":self.index_ready,
            "llm_configured":self.llm_configured
        }
