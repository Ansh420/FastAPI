import requests
from bs4 import BeautifulSoup
import uuid
from fastapi import FastAPI, Body
from PyPDF2 import PdfReader 
app = FastAPI()

# Function to scrape and clean content
def scrape_and_clean_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove scripts and styles (optional, customize based on your needs)
        for script in soup(["script", "style"]):
            script.extract()

        # Extract text content from relevant elements
        text = soup.get_text(separator='\n')

        return text.strip()  # Remove leading/trailing whitespace

    except requests.exceptions.RequestException as e:
        print(f"Error scraping URL: {e}")
        return None

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Create a database engine (replace with your database connection string)
engine = create_engine('sqlite:///scraped_data.db')

class ScrapedContent(Base):
    __tablename__ = 'scraped_content'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String)
    content = Column(String)

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)

@app.post("/process_url")
async def process_web_url(url: str = Body('https://en.wikipedia.org/wiki/Technology')):
    """
    Scrapes content from a given URL and stores it.

    Args:
        url (str): The URL to scrape content from.

    Returns:
        dict: A dictionary containing the chat_id and success message.
    """    
    cleaned_content = scrape_and_clean_content(url)

    if cleaned_content is None:
        return {"message": "Failed to scrape content from the provided URL."}, 500

    # Generate a unique chat ID
    chat_id = str(uuid.uuid4())

    session = Session()

    # Create a new ScrapedContent instance and add it to the session
    scraped_content = ScrapedContent(chat_id=chat_id, content=cleaned_content)
    session.add(scraped_content)

    # Commit the changes to the database
    session.commit()

    session.close()

    return {"chat_id": chat_id, "message": "URL content processed and stored successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)