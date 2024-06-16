from app.modules.chat_module import ChatModule
from app.modules.api_module import APIModule
from app.modules.search_module import SearchModule
from app.modules.wiki_summary_module import WikiSummaryModule
from app.modules.wikipedia_query_module import WikipediaQueryModule
from srt_core.config import Config
from srt_core.utils.logger import Logger


def main():
    config = Config()
    logger = Logger()

    chat_module = ChatModule(config, logger)

    # Initialize APIModule with error handling
    try:
        api_module = APIModule(config, logger)
    except ImportError as e:
        api_module = None
        logger.info(f"API module could not be imported: {e}. API functionality is disabled.")

    # Initialize SearchModule with error handling
    try:
        search_module = SearchModule(config, logger)
    except ImportError as e:
        search_module = None
        logger.info(f"Search module could not be initialized: {e}. Search functionality is disabled.")

    # Initialize WikiSummaryModule with error handling
    try:
        wiki_summary_module = WikiSummaryModule(config, logger)
    except ImportError as e:
        wiki_summary_module = None
        logger.info(f"WikiSummary module could not be initialized: {e}. WikiSummary functionality is disabled.")

    # Initialize WikipediaQueryModule with error handling
    try:
        wikipedia_query_module = WikipediaQueryModule(config, logger)
    except ImportError as e:
        wikipedia_query_module = None
        logger.info(f"Wikipedia Query module could not be initialized: {e}. Wikipedia Query functionality is disabled.")

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
                query = user_input[len("search:"):].strip()
                results = search_module.search(query)
                print(f"Search Results: {results}")
            else:
                print("Search functionality is disabled due to missing dependencies.")
        elif user_input.startswith("wiki:"):
            if wiki_summary_module:
                page_title = user_input[len("wiki:"):].strip()
                summary = wiki_summary_module.summarize_wikipedia_page(page_title)
                print(f"Summary: {summary}")
            else:
                print("WikiSummary functionality is disabled due to import issues.")
        elif user_input.startswith("wikipedia_query:"):
            if wikipedia_query_module:
                inputs = user_input[len("wikipedia_query:"):].strip().split(",", 1)
                if len(inputs) == 2:
                    page_url, query = inputs
                    result = wikipedia_query_module.process_wikipedia_query(page_url.strip(), query.strip())
                    print(f"Query Result: {result}")
                else:
                    print("Please provide both the Wikipedia page URL and the query, separated by a comma.")
            else:
                print("Wikipedia Query functionality is disabled due to import issues.")
        else:
            response = chat_module.chat(user_input)
            print(f"Agent: {response}")


if __name__ == "__main__":
    main()
