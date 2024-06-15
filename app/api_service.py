import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.modules.chat_module import ChatModule
from srt_core.config import Config
from srt_core.utils.logger import Logger
import logging

app = FastAPI()

config = Config()
logger = Logger()

chat_module = ChatModule(config, logger)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def health_check():
    logger.log(logging.DEBUG, "Health check endpoint called")
    return {"message": "Welcome to the srt-web-chat API"}

@app.get("/fetch")
def fetch_data(url: str):
    logger.log(logging.DEBUG, f"Fetching data from URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.log(logging.ERROR, f"Error fetching data from URL: {url}, error: {e}")
        raise HTTPException(status_code=404, detail="Error fetching data")

@app.get("/fetch-list")
def fetch_data_list(url: str):
    logger.log(logging.DEBUG, f"Fetching list from URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.log(logging.ERROR, f"Error fetching list from URL: {url}, error: {e}")
        raise HTTPException(status_code=404, detail="Error fetching data list")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = chat_module.chat(request.message)
        return {"response": response}
    except Exception as e:
        logger.log(logging.ERROR, f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/wiki-summary/{title}")
def wiki_summary(title: str):
    logger.log(logging.DEBUG, f"Fetching wiki summary for title: {title}")
    # Implement wiki summary logic here
    return {"summary": "WikiSummary functionality is disabled due to missing dependencies."}
