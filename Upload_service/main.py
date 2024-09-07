from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
import requests
from bs4 import BeautifulSoup
import multipart


app = FastAPI()

# In-memory storage for documents
documents = {}

class ChatRequest(BaseModel):
    chat_id: str
    question: str

class Document(BaseModel):
    chat_id: str
    content: str

@app.post("/upload_url/")
async def upload_url(chat_id: str = Form(...), url: str = Form(...)):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract text from the main content of the HTML
    for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
        script.extract()  # Remove these tags and their content
    content = ' '.join(soup.stripped_strings)
    documents[chat_id] = content
    return {"message": "Document uploaded successfully"}

@app.post("/upload_pdf/")
async def upload_pdf(chat_id: str = Form(...), file: UploadFile = File(...)):
    content = extract_text(file.file)
    documents[chat_id] = content
    return {"message": "Document uploaded successfully"}

@app.post("/chat/")
async def chat(request: ChatRequest):
    chat_id = request.chat_id
    question = request.question

    if chat_id not in documents:
        return {"response": "Document not found"}

    document_content = documents[chat_id]
    response = find_most_relevant_section(document_content, question)
    return {"response": response}

def find_most_relevant_section(document: str, query: str) -> str:
    # Split document into smaller sections
    sections = document.split('\n\n')
    section_embeddings = [embed_text(section) for section in sections]
    query_embedding = embed_text(query)

    # Compute cosine similarity
    similarities = cosine_similarity([query_embedding], section_embeddings)
    most_relevant_index = np.argmax(similarities)

    return sections[most_relevant_index]

def embed_text(text: str) -> np.ndarray:
    # Dummy embedding function (replace with actual embedding logic)
    return np.random.rand(300)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
