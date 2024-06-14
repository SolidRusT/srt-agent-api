from srt_core.config import Config
from srt_core.utils.logger import Logger
from basic_chat import BasicChat

config = Config()
logger = Logger()

if config.debug:
    print("Debug mode is enabled")

chat_module = BasicChat(config)

# Try to import and initialize SearchModule
try:
    from search_module import SearchModule
    search_module = SearchModule(config)
except ImportError as e:
    search_module = None
    logger.info(f"Search module dependencies are not installed: {e}. Search functionality is disabled.")

while True:
    user_input = input(">")
    if user_input == "exit":
        break
    elif user_input.startswith("search:"):
        if search_module:
            query = user_input[len("search:"):].strip()
            results = search_module.search(query)
            print(f"Search Results: {results}")
        else:
            print("Search functionality is disabled due to missing dependencies.")
    else:
        response = chat_module.chat(user_input)
        print(f"Agent: {response}")
