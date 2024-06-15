from srt_core.config import Config
from srt_core.utils.logger import Logger
from app.modules.chat_module import ChatModule

config = Config()
logger = Logger()

if config.debug:
    print("Debug mode is enabled")

chat_module = ChatModule(config, logger)

# Try to import and initialize APIModule
try:
    from app.modules.api_module import APIModule
    api_module = APIModule(config, logger)
except ImportError as e:
    api_module = None
    logger.info(f"API module could not be imported: {e}. API functionality is disabled.")

# Try to import and initialize SearchModule
try:
    from app.modules.search_module import SearchModule
    search_module = SearchModule(config, logger)
except ImportError as e:
    search_module = None
    logger.info(
        f"Search module could not be initialized: {e}. Search functionality is disabled."
    )

# Try to import and initialize WikiSummaryModule
try:
    from app.modules.wiki_summary_module import WikiSummaryModule
    wiki_summary_module = WikiSummaryModule(config, logger)
except ImportError as e:
    wiki_summary_module = None
    logger.info(
        f"WikiSummary module could not be initialized: {e}. WikiSummary functionality is disabled."
    )

while True:
    user_input = input(">")
    if user_input == "exit":
        break
    elif user_input.startswith("fetch:"):
        if api_module:
            url = user_input[len("fetch:"):].strip()
            data = api_module.fetch_data(url)
            print(f"Fetched Data: {data}")
        else:
            print("API functionality is disabled due to import issues.")
    elif user_input.startswith("fetch_list:"):
        if api_module:
            url = user_input[len("fetch_list:"):].strip()
            data_list = api_module.fetch_data_list(url)
            print(f"Fetched Data List: {data_list}")
        else:
            print("API functionality is disabled due to import issues.")
    elif user_input.startswith("search:"):
        if search_module:
            query = user_input[len("search:") :].strip()
            results = search_module.search(query)
            print(f"Search Results: {results}")
        else:
            print("Search functionality is disabled due to missing dependencies.")
    elif user_input.startswith("wiki:"):
        if wiki_summary_module:
            page_title = user_input[len("wiki:") :].strip()
            summary = wiki_summary_module.summarize_wikipedia_page(page_title)
            print(f"Summary: {summary}")
        else:
            print("WikiSummary functionality is disabled due to import issues.")
    else:
        response = chat_module.chat(user_input)
        print(f"Agent: {response}")
