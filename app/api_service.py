from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.modules.chat_module import ChatModule
from app.modules.api_module import APIModule
from app.modules.search_module import SearchModule
from app.modules.wiki_summary_module import WikiSummaryModule
from app.modules.wikipedia_query_module import WikipediaQueryModule
from app.modules.product_comparison_module import ProductComparisonModule
from srt_core.config import Config
from srt_core.utils.logger import Logger
import uvicorn

app = FastAPI(
    title="SRT Agent API",
    description="A modular web chat application integrating srt-core and llama-cpp-agent frameworks.",
    version="0.1.5",
    contact={
        "name": "SolidRusT Networks",
        "url": "https://github.com/SolidRusT/srt-agent-api",
        "email": "suparious@solidrust.net",
    },
)

config = Config()
logger = Logger()
chat_module = ChatModule(config, logger)

server_name = config.server_name
server_port = config.server_port
logger.info(f"Starting API service on: {server_name}:{server_port}.")

# Initialize modules with error handling
try:
    api_module = APIModule(config, logger)
except ImportError as e:
    api_module = None
    logger.info(f"API module could not be imported: {e}. API functionality is disabled.")

try:
    search_module = SearchModule(config, logger)
except ImportError as e:
    search_module = None
    logger.info(f"Search module could not be initialized: {e}. Search functionality is disabled.")

try:
    wiki_summary_module = WikiSummaryModule(config, logger)
except ImportError as e:
    wiki_summary_module = None
    logger.info(f"WikiSummary module could not be initialized: {e}. WikiSummary functionality is disabled.")

try:
    wikipedia_query_module = WikipediaQueryModule(config, logger)
except ImportError as e:
    wikipedia_query_module = None
    logger.info(f"Wikipedia Query module could not be initialized: {e}. Wikipedia Query functionality is disabled.")

try:
    product_comparison_module = ProductComparisonModule(config, logger)
except ImportError as e:
    product_comparison_module = None
    logger.info(f"Product Comparison module could not be initialized: {e}. Product Comparison functionality is disabled.")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/", summary="Health Check", tags=["Health"])
def health_check():
    logger.debug("Health check endpoint called")
    return {"message": "Welcome to the srt-web-chat API"}

@app.post("/chat", response_model=ChatResponse, summary="Chat with the Agent", tags=["Chat Module"])
async def chat(request: ChatRequest):
    try:
        response = chat_module.chat(request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/fetch", summary="Fetch Data", tags=["API Module"])
def fetch_data(url: str = Query(..., description="URL to fetch data from")):
    if not api_module:
        raise HTTPException(status_code=501, detail="API functionality is disabled.")
    logger.debug(f"Fetching data from URL: {url}")
    try:
        response = api_module.fetch_data(url)
        return response
    except Exception as e:
        logger.error(f"Error fetching data from URL: {url}, error: {e}")
        raise HTTPException(status_code=404, detail="Error fetching data")

@app.get("/fetch-list", summary="Fetch Data List", tags=["API Module"])
def fetch_data_list(url: str = Query(..., description="URL to fetch list data from")):
    if not api_module:
        raise HTTPException(status_code=501, detail="API functionality is disabled.")
    logger.debug(f"Fetching list from URL: {url}")
    try:
        response = api_module.fetch_data_list(url)
        return response
    except Exception as e:
        logger.error(f"Error fetching list from URL: {url}, error: {e}")
        raise HTTPException(status_code=404, detail="Error fetching data list")

@app.get("/search", summary="Perform a Web Search", tags=["Search Module"])
def search(query: str = Query(..., description="Query to search for")):
    if not search_module:
        raise HTTPException(status_code=501, detail="Search functionality is disabled.")
    logger.debug(f"Performing search for query: {query}")
    try:
        results = search_module.search(query)
        return {"results": results}
    except Exception as e:
        logger.error(f"Error performing search for query: {query}, error: {e}")
        raise HTTPException(status_code=500, detail="Error performing search")

@app.get("/wiki-summary/{title}", summary="Get Wikipedia Summary", tags=["Wiki Summary Module"])
def wiki_summary(title: str):
    if not wiki_summary_module:
        raise HTTPException(status_code=501, detail="WikiSummary functionality is disabled.")
    logger.debug(f"Fetching wiki summary for title: {title}")
    try:
        summary = wiki_summary_module.summarize_wikipedia_page(title)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error fetching wiki summary for title: {title}, error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching wiki summary")

@app.get("/wikipedia-query", summary="Query Wikipedia Page", tags=["Wikipedia Query Module"])
def wikipedia_query(page_url: str, query: str):
    if not wikipedia_query_module:
        raise HTTPException(status_code=501, detail="Wikipedia Query functionality is disabled.")
    logger.debug(f"Processing Wikipedia query for page: {page_url} and query: {query}")
    try:
        result = wikipedia_query_module.process_wikipedia_query(page_url, query)
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing Wikipedia query for page: {page_url} and query: {query}, error: {e}")
        raise HTTPException(status_code=500, detail="Error processing Wikipedia query")

@app.get("/product-comparison", summary="Compare Products and Recommend", tags=["Product Comparison Module"])
def product_comparison(product1: str, product2: str, category: str, user_profile: str):
    if not product_comparison_module:
        raise HTTPException(status_code=501, detail="Product Comparison functionality is disabled.")
    logger.debug(f"Processing product comparison for: {product1} vs {product2} in category {category} for user {user_profile}")
    try:
        result = product_comparison_module.compare_and_recommend(product1, product2, category, user_profile)
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing product comparison: {e}")
        raise HTTPException(status_code=500, detail="Error processing product comparison")


if __name__ == "__main__":
    uvicorn.run("app.api_service:app", host=server_name, port=server_port, reload=True, app_dir=".")
