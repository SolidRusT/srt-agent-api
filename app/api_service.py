from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

@app.get("/")
def health_check():
    logging.debug("Health check endpoint called")
    return {"message": "Welcome to the srt-web-chat API"}

@app.get("/fetch")
def fetch_data(url: str):
    logging.debug(f"Fetching data from URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching data from URL: {url}, error: {e}")
        raise HTTPException(status_code=404, detail="Error fetching data")

@app.get("/fetch-list")
def fetch_data_list(url: str):
    logging.debug(f"Fetching list from URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching list from URL: {url}, error: {e}")
        raise HTTPException(status_code=404, detail="Error fetching data list")

@app.get("/wiki-summary/{title}")
def wiki_summary(title: str):
    logging.debug(f"Fetching wiki summary for title: {title}")
    # Implement wiki summary logic here
    return {"summary": "WikiSummary functionality is disabled due to missing dependencies."}
