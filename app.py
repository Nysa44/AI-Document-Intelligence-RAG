import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from rag.engine import RAGEngine

load_dotenv()
app=Flask(__name__)
app.config["MAX_CONTENT_LENGTH"]=int(os.getenv("MAX_UPLOAD_MB","30"))*1024*1024
engine=RAGEngine()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({
        "status":"healthy",
        "index_ready":engine.index_ready,
        "llm_configured":engine.llm_configured
    })

@app.get("/api/stats")
def stats():
    return jsonify(engine.stats())

@app.post("/api/upload")
def upload():
    files=request.files.getlist("files")
    if not files:
        return jsonify({"error":"No files supplied."}),400
    return jsonify(engine.ingest_files(files))

@app.post("/api/query")
def query():
    payload=request.get_json(silent=True) or {}
    question=str(payload.get("question","")).strip()
    if not question:
        return jsonify({"error":"Question is required."}),400
    try:
        return jsonify(engine.ask(question))
    except Exception as exc:
        return jsonify({"error":str(exc)}),500

if __name__=="__main__":
    os.makedirs("data/uploads",exist_ok=True)
    os.makedirs("data/index",exist_ok=True)
    engine.build_index()
    app.run(host="0.0.0.0",port=5000,debug=True)
