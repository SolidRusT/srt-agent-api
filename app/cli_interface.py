from app.modules.chat_module import ChatModule
from app.modules.api_module import APIModule
from app.modules.search_module import SearchModule
from app.modules.wiki_summary_module import WikiSummaryModule
from app.modules.wikipedia_query_module import WikipediaQueryModule
from app.modules.product_comparison_module import ProductComparisonModule
from app.modules.agentic_reflection_module import AgenticReflectionModule
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

    # Initialize ProductComparisonModule with error handling
    try:
        product_comparison_module = ProductComparisonModule(config, logger)
    except ImportError as e:
        product_comparison_module = None
        logger.info(f"Product Comparison module could not be initialized: {e}. Product Comparison functionality is disabled.")

    # Initialize AgenticReflectionModule with error handling
    try:
        agentic_reflection_module = AgenticReflectionModule(config, logger)
    except ImportError as e:
        agentic_reflection_module = None
        logger.info(f"Agentic Reflection module could not be initialized: {e}. Reflection functionality is disabled.")

    while True:
        user_input = input("> ")

        if user_input == "exit":
            break
        elif user_input.startswith("fetch:"):
            if api_module:
                url = user_input[len("fetch:"):].strip()
                try:
                    data = api_module.fetch_data(url)
                    print(f"Fetched Data: {data}")
                except Exception as e:
                    print(f"Error fetching data: {e}")
            else:
                print("API functionality is disabled due to import issues.")
        elif user_input.startswith("fetch_list:"):
            if api_module:
                url = user_input[len("fetch_list:"):].strip()
                try:
                    data_list = api_module.fetch_data_list(url)
                    print(f"Fetched Data List: {data_list}")
                except Exception as e:
                    print(f"Error fetching data list: {e}")
            else:
                print("API functionality is disabled due to import issues.")
        elif user_input.startswith("search:"):
            if search_module:
                query = user_input[len("search:"):].strip()
                try:
                    results = search_module.search(query)
                    print(f"Search Results: {results}")
                except Exception as e:
                    print(f"Error performing search: {e}")
            else:
                print("Search functionality is disabled due to missing dependencies.")
        elif user_input.startswith("wiki:"):
            if wiki_summary_module:
                page_title = user_input[len("wiki:"):].strip()
                try:
                    summary = wiki_summary_module.summarize_wikipedia_page(page_title)
                    print(f"Summary: {summary}")
                except Exception as e:
                    print(f"Error fetching wiki summary: {e}")
            else:
                print("WikiSummary functionality is disabled due to import issues.")
        elif user_input.startswith("wikipedia_query:"):
            if wikipedia_query_module:
                inputs = user_input[len("wikipedia_query:"):].strip().split(",", 1)
                if len(inputs) == 2:
                    page_url, query = inputs
                    try:
                        result = wikipedia_query_module.process_wikipedia_query(page_url.strip(), query.strip())
                        print(f"Query Result: {result}")
                    except Exception as e:
                        print(f"Error processing wikipedia query: {e}")
                else:
                    print("Please provide both the Wikipedia page URL and the query, separated by a comma.")
            else:
                print("Wikipedia Query functionality is disabled due to import issues.")
        elif user_input.startswith("compare:"):
            if product_comparison_module:
                params = user_input[len("compare:"):].strip().split(",")
                if len(params) == 4:
                    product1, product2, category, user_profile = params
                    try:
                        result = product_comparison_module.compare_and_recommend(product1.strip(), product2.strip(),
                                                                                 category.strip(), user_profile.strip())
                        print(f"Product Comparison Result: {result}")
                    except Exception as e:
                        print(f"Error performing product comparison: {e}")
                else:
                    print("Invalid input format. Use: compare: product1, product2, category, user_profile")
            else:
                print("Product Comparison functionality is disabled due to import issues.")
        elif user_input.startswith("reflect:"):
            if agentic_reflection_module:
                input_message = user_input[len("reflect:"):].strip()
                try:
                    response = agentic_reflection_module.get_reflective_response(input_message)
                    print(f"Reflective Response: {response}")
                except Exception as e:
                    print(f"Error processing reflective response: {e}")
            else:
                print("Reflection functionality is disabled due to missing dependencies.")
        else:
            # Universal chat handling with function calling
            try:
                response = chat_module.chat(user_input)
                print(f"Agent: {response}")
            except Exception as e:
                print(f"Error in chat module: {e}")

if __name__ == "__main__":
    main()
