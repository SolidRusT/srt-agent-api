import datetime
from typing import Union, Optional

from llama_cpp_agent import FunctionCallingAgent, LlamaCppFunctionTool
from llama_cpp_agent.messages_formatter import MessagesFormatterType
from app.modules.base_module import BaseModule
from app.modules.api_module import APIModule
from app.modules.wiki_summary_module import WikiSummaryModule
from app.modules.wikipedia_query_module import WikipediaQueryModule
from app.modules.agentic_reflection_module import AgenticReflectionModule

class ChatModule(BaseModule):
    def __init__(self, config, logger):
        super().__init__(config, logger, ["llama_cpp_agent"])
        if self.dependencies_available:
            self.provider = self._initialize_provider(config.default_llm_settings)
            self.function_calling_agent = self._initialize_function_calling_agent()
            #TODO: debug toggle: self.function_calling_agent.structured_output_settings.output_raw_json_string = True

    def _initialize_function_calling_agent(self):
        tools = [
            LlamaCppFunctionTool(self._get_current_datetime),
            LlamaCppFunctionTool(self._perform_calculations),
            LlamaCppFunctionTool(self._fetch_data),
            LlamaCppFunctionTool(self._wiki_summary),
            LlamaCppFunctionTool(self._wikipedia_query),
            LlamaCppFunctionTool(self._reflective_response)
        ]
        return FunctionCallingAgent(
            self.provider,
            llama_cpp_function_tools=tools,
            send_message_to_user_callback=self._send_message_to_user_callback,
            allow_parallel_function_calling=True,
            debug_output=False,
            messages_formatter_type=MessagesFormatterType.MISTRAL
        )

    def _send_message_to_user_callback(self, message: str):
        self.logger.info(f"Assistant: {message.strip()}")

    def _get_current_datetime(self, output_format: Optional[str] = None):
        """
        Get the current date and time in the given format.

        Args:
            output_format (str, optional): The format for the output datetime string.

        Returns:
            str: The formatted current datetime string.
        """
        if output_format is None:
            output_format = '%Y-%m-%d %H:%M:%S'
        return datetime.datetime.now().strftime(output_format)

    def _perform_calculations(self, number_one: Union[int, float], operation: str, number_two: Union[int, float]):
        """
        Perform a calculation with two numbers.

        Args:
            number_one (Union[int, float]): The first number.
            operation (str): The operation to perform ('add', 'subtract', 'multiply', 'divide').
            number_two (Union[int, float]): The second number.

        Returns:
            Union[int, float]: The result of the calculation.
        """
        if operation == "add":
            return number_one + number_two
        elif operation == "subtract":
            return number_one - number_two
        elif operation == "multiply":
            return number_one * number_two
        elif operation == "divide":
            return number_one / number_two
        else:
            raise ValueError("Unknown operation.")

    def _fetch_data(self, url: str):
        """
        Fetch data from a given URL.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            dict: The fetched data.
        """
        api_module = APIModule(self.config, self.logger)
        return api_module.fetch_data(url)

    def _wiki_summary(self, page_title: str):
        """
        Get a summary of a Wikipedia page.

        Args:
            page_title (str): The title of the Wikipedia page.

        Returns:
            str: The summary of the Wikipedia page.
        """
        wiki_summary_module = WikiSummaryModule(self.config, self.logger)
        return wiki_summary_module.summarize_wikipedia_page(page_title)

    def _wikipedia_query(self, page_url: str, query: str):
        """
        Query a Wikipedia page.

        Args:
            page_url (str): The URL of the Wikipedia page.
            query (str): The query to perform on the page.

        Returns:
            str: The result of the query.
        """
        wikipedia_query_module = WikipediaQueryModule(self.config, self.logger)
        return wikipedia_query_module.process_wikipedia_query(page_url, query)

    def _reflective_response(self, input_message: str):
        """
        Get a reflective response for a given input message.

        Args:
            input_message (str): The input message to reflect upon.

        Returns:
            str: The reflective response.
        """
        agentic_reflection_module = AgenticReflectionModule(self.config, self.logger)
        return agentic_reflection_module.get_reflective_response(input_message)

    def chat(self, user_input: str):
        settings = self.provider.get_provider_default_settings()
        settings.stream = False
        settings.temperature = 0.65
        settings.max_tokens = 2048

        return self.function_calling_agent.generate_response(user_input, llm_sampling_settings=settings)

# Example usage
if __name__ == "__main__":
    from srt_core.config import Config
    from srt_core.utils.logger import Logger

    config = Config()
    logger = Logger()
    chat_module = ChatModule(config, logger)
    print(chat_module.chat("What is the current date and time?"))
