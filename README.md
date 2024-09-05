# FastAPI
## scraping content from a given URL 
storing it in a database using SQLAlchemy, within the context of a FastAPI application. It incorporates the following key functionalities:

# **URL Scraping**: 

- Extracts content from a specified URL using the requests library.
- Cleans the extracted content by removing scripts and styles (if desired).
# **SQLAlchemy Integration**:

- Creates a database engine and defines a SQLAlchemy model to represent the scraped data.
- Creates a database table based on the model.
- Uses a database session to add and commit scraped content to the database.
# **FastAPI Endpoint**:

- Exposes a POST endpoint (/process_url) that accepts a URL as input.
- Processes the URL, scrapes the content, and stores it in the database.
- Returns a response with a unique chat ID and a success message.
# **Error Handling**:

- Implements basic error handling for HTTP requests and database operations.

 ## **Extract text from uploaded pdf**
 **Q&A Chatbot with Document Upload**
- This is a FastAPI application for a simple Q&A chatbot that leverages uploaded documents.

**Features**:

- Supports uploading documents through URLs or PDFs.
- Extracts text content from uploaded documents.
- Processes user chat requests with a specific chat ID.
- Finds the most relevant section within the uploaded document based on the user's question using cosine similarity (Note: currently uses a dummy embedding function, needs replacement).
