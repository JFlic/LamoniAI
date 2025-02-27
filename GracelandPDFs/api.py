from fastapi import FastAPI
from pydantic import BaseModel
from retrieve import rag_chain, clip_text  # Import retrieval logic from retrieve.py

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    resp_dict = rag_chain.invoke({"input": request.question})
    clipped_answer = clip_text(resp_dict["answer"], threshold=1000)
    
    sources = [
        {
            "text": clip_text(doc.page_content, threshold=500),
            "article_name": doc.metadata.get("dl_meta", {}).get("origin", {}).get("filename", "Unknown").split(".")[0],
            "page_number": doc.metadata.get("dl_meta", {}).get("doc_items", [{}])[0].get("prov", [{}])[0].get("page_no", "Unknown")
        }
        for doc in resp_dict["context"]
    ]

    return {"question": request.question, "answer": clipped_answer, "sources": sources}
