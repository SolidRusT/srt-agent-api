import requests
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.modules.chat_module import ChatModule
from srt_core.config import Config
from srt_core.utils.logger import Logger

app = FastAPI(
    title="srt-web-chat API",
    description="A modular web chat application integrating srt-core and llama-cpp-agent frameworks.",
    version="0.1.2",
    contact={
        "name": "SolidRusT Networks",
        "url": "https://github.com/SolidRusT/srt-web-chat",
        "email": "info@solidrust.net",
    },
)

config = Config()
logger = Logger()
chat_module = ChatModule(config, logger)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/", summary="Health Check", tags=["Health"])
def health_check():
    logger.debug("Health check endpoint called")
    return {"message": "Welcome to the srt-web-chat API"}

@app.get("/fetch", summary="Fetch Data", tags=["API Module"])
def fetch_data(url: str = Query(..., description="URL to fetch data from")):
    logger.debug(f"Fetching data from URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from URL: {url}, error: {e}")
        raise HTTPException(status_code=404, detail="Error fetching data")

@app.get("/fetch-list", summary="Fetch Data List", tags=["API Module"])
def fetch_data_list(url: str = Query(..., description="URL to fetch list data from")):
    logger.debug(f"Fetching list from URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching list from URL: {url}, error: {e}")
        raise HTTPException(status_code=404, detail="Error fetching data list")

@app.post("/chat", response_model=ChatResponse, summary="Chat with the Agent", tags=["Chat Module"])
async def chat(request: ChatRequest):
    try:
        response = chat_module.chat(request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/wiki-summary/{title}", summary="Get Wikipedia Summary", tags=["Wiki Summary Module"])
def wiki_summary(title: str):
    logger.debug(f"Fetching wiki summary for title: {title}")
    # Implement wiki summary logic here
    return {"summary": "WikiSummary functionality is disabled due to missing dependencies."}
