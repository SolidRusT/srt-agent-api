from srt_core.config import Config
from srt_core.utils.logger import Logger
from chat_module import ChatModule

config = Config()
logger = Logger()

if config.debug:
    print("Debug mode is enabled")

chat_module = ChatModule(config, logger)

# Try to import and initialize APIModule
try:
    from api_module import APIModule
    api_module = APIModule(config, logger)
except ImportError as e:
    api_module = None
    logger.info(f"API module could not be imported: {e}. API functionality is disabled.")


# Try to import and initialize SearchModule
try:
    from search_module import SearchModule
    search_module = SearchModule(config, logger)
except ImportError as e:
    search_module = None
    logger.info(
        f"Search module could not be initialized: {e}. Search functionality is disabled."
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
    elif user_input.startswith("search:"):
        if search_module:
            query = user_input[len("search:") :].strip()
            results = search_module.search(query)
            print(f"Search Results: {results}")
        else:
            print("Search functionality is disabled due to missing dependencies.")
    else:
        response = chat_module.chat(user_input)
        print(f"Agent: {response}")
