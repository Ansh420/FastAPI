from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
import PyPDF2
import re

app = FastAPI()

# In-memory storage for simplicity
pdf_storage = {}

@app.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
    
    try:
        # Read the PDF file using PdfReader
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        
        # Clean the text
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        
        # Generate a unique chat_id
        chat_id = str(uuid4())
        
        # Store the cleaned text with the chat_id
        pdf_storage[chat_id] = cleaned_text
        
        return JSONResponse(content={"chat_id": chat_id, "message": "PDF content processed and stored successfully."})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the PDF: {str(e)}")

# Endpoint to retrieve stored PDF content by chat_id
@app.get("/get_pdf_content/{chat_id}")
async def get_pdf_content(chat_id: str):
    if chat_id not in pdf_storage:
        raise HTTPException(status_code=404, detail="Chat ID not found.")
    
    return JSONResponse(content={"chat_id": chat_id, "content": pdf_storage[chat_id]})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
