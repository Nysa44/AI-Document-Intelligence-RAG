import os
from openai import OpenAI

class AnswerGenerator:
    def __init__(self):
        key=os.getenv("OPENAI_API_KEY")
        self.model=os.getenv("OPENAI_MODEL","gpt-4o-mini")
        self.client=OpenAI(api_key=key) if key else None

    @property
    def configured(self):
        return self.client is not None

    def generate(self,question,contexts):
        if not contexts:
            return "I could not find relevant information in the indexed documents."

        context="\n\n".join(
            f"[Source: {x['source']}, chunk {x['chunk_id']}"
            + (f", page {x['page']}]" if x.get("page") else "]")
            + f"\n{x['text']}"
            for x in contexts
        )

        if not self.client:
            return ("LLM API key is not configured. Semantic retrieval succeeded.\n\n"
                    "Most relevant retrieved context:\n\n"+context[:8000])

        system=("You are a document intelligence assistant. "
                "Answer ONLY from the supplied context. Do not invent facts. "
                "If the answer is unsupported, say it was not found. "
                "Cite supporting sources as [filename, chunk N] and page numbers when available.")

        response=self.client.chat.completions.create(
            model=self.model,
            temperature=0.1,
            messages=[
                {"role":"system","content":system},
                {"role":"user","content":f"DOCUMENT CONTEXT:\n{context}\n\nQUESTION:\n{question}"}
            ]
        )
        return response.choices[0].message.content
