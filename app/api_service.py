from fastapi import FastAPI
from app.modules.wiki_summary_module import WikiSummaryModule
from srt_core.config import Config
from srt_core.utils.logger import Logger

config = Config()
logger = Logger()

app = FastAPI()

# Initialize WikiSummaryModule
try:
    wiki_summary_module = WikiSummaryModule(config, logger)
except ImportError as e:
    wiki_summary_module = None
    logger.info(
        f"WikiSummary module could not be initialized: {e}. WikiSummary functionality is disabled."
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the srt-web-chat API"}

@app.get("/wiki-summary/{title}")
def get_wiki_summary(title: str):
    if wiki_summary_module:
        summary = wiki_summary_module.summarize_wikipedia_page(title)
        return {"summary": summary}
    else:
        return {"error": "WikiSummary functionality is disabled due to missing dependencies"}
