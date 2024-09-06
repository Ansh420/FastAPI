# FastAPI
# **scraping content from a given URL** 
storing it in a database using SQLAlchemy, within the context of a FastAPI application. It incorporates the following key functionalities:

## URL Scraping: 

- Extracts content from a specified URL using the requests library.
- Cleans the extracted content by removing scripts and styles (if desired).
## SQLAlchemy Integration:

- Creates a database engine and defines a SQLAlchemy model to represent the scraped data.
- Creates a database table based on the model.
- Uses a database session to add and commit scraped content to the database.
## FastAPI Endpoint:

- Exposes a POST endpoint (/process_url) that accepts a URL as input.
- Processes the URL, scrapes the content, and stores it in the database.
- Returns a response with a unique chat ID and a success message.
## Error Handling:

- Implements basic error handling for HTTP requests and database operations.

 # **Extract text from uploaded pdf**
 ## Q&A Chatbot with Document Upload
- This is a FastAPI application for a simple Q&A chatbot that leverages uploaded documents.

## Features:

- Supports uploading documents through URLs or PDFs.
- Extracts text content from uploaded documents.
- Processes user chat requests with a specific chat ID.
- Finds the most relevant section within the uploaded document based on the user's question using cosine similarity (Note: currently uses a dummy embedding function, needs replacement).

# **FastAPI Chatbot with Document Upload**
This project implements a simple chatbot that retrieves relevant information from uploaded documents.

## Features:

- Supports uploading documents through URLs or PDFs.
- Extracts text content from uploaded documents.
- Processes user questions and identifies the most relevant section based on cosine similarity.

## Technologies:

- FastAPI: Web framework for building APIs
- Pydantic: Data validation and serialization
- requests: Making HTTP requests
- BeautifulSoup: Parsing HTML documents
- pdfminer: Extracting text from PDFs

## Usage:

### Run the application:
$Bash

$ uvicorn main:app --host 127.0.0.1 --port 8000


### Upload documents:
### Upload URL:
$ Bash
$ curl -X POST http://localhost:8000/upload_url/ -F chat_id=user1 -F url=https://www.example.com/article.html

## Upload PDF: (using tools like curl or Postman)
Set chat_id in the form data.
Send a multipart request with the PDF file as file.
## Chat interaction:
$ Bash
$ curl -X POST http://localhost:8000/chat/ -H 'Content-Type: application/json' -d '{"chat_id": "user1", "question": "What is the capital of France?"}'

## Return
This will return a JSON response containing the most relevant section from the uploaded document for user1 based on the question. 



