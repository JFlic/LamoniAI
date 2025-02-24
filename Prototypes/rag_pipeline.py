import os
import faiss
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel, pipeline

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-large-v2")
model = AutoModel.from_pretrained("intfloat/e5-large-v2")

# Load FAISS index
index = faiss.read_index("faiss_index.bin")

def compute_query_embedding(query):
    """Computes embedding for a given query."""
    batch_dict = tokenizer([query], padding=True, truncation=True, return_tensors="pt", max_length=512)
    outputs = model(**batch_dict)

    last_hidden = outputs.last_hidden_state.masked_fill(~batch_dict['attention_mask'][..., None].bool(), 0.0)
    embedding = last_hidden.sum(dim=1) / batch_dict['attention_mask'].sum(dim=1)[..., None]

    return F.normalize(embedding, p=2, dim=1).detach().numpy()

def retrieve_top_k(query, text_directory, k=3):
    """Retrieves the top-k most relevant documents."""
    texts, filenames = [], []
    
    # Load saved texts
    for filename in os.listdir(text_directory):
        if filename.endswith(".md"):
            file_path = os.path.join(text_directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                texts.append(file.read())
                filenames.append(filename)

    # Compute query embedding
    query_embedding = compute_query_embedding(query)

    # Search FAISS index
    distances, indices = index.search(query_embedding, k)

    retrieved_texts = [texts[idx] for idx in indices[0] if idx < len(texts)]
    return retrieved_texts

def generate_response(query, retrieved_texts):
    """Generates an AI response using LLM based on retrieved context."""
    context = "\n".join(retrieved_texts)
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

    llm = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct", torch_dtype=torch.float16, device=0)
    response = llm(prompt, max_length=200, do_sample=True, temperature=0.7)

    return response[0]["generated_text"]

# Run RAG pipeline
if __name__ == "__main__":
    query = "What events happened at Graceland University in 2009?"
    text_directory = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\ExtractedText"

    retrieved_texts = retrieve_top_k(query, text_directory)

    if retrieved_texts:
        print("Generating response...")
        final_response = generate_response(query, retrieved_texts)
        print("\n🔹 AI Response:\n", final_response)
    else:
        print("❌ No relevant documents found!")
