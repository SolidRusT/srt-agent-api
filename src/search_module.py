import importlib.util
from srt_core.config import Config
from srt_core.utils.logger import Logger

class SearchModule:
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
        import logging
        self.logging = logging
        self.dependencies_available = self._check_dependencies()
        
        if self.dependencies_available:
            self.provider = self._initialize_provider()
            self.agent = self._initialize_agent()
            self.search_tool = self._initialize_search_tool()
            self.settings = self.provider.get_provider_default_settings()
            self._configure_settings()
            self.output_settings = LlmStructuredOutputSettings.from_functions(
                [self.search_tool.get_tool(), self.write_message_to_user]
            )
        else:
            self.logging.info("Search tool dependencies are not installed. Disabling search functionality.")

    def _check_dependencies(self):
        required_modules = ["llama_cpp_agent", "readability", "trafilatura"]
        for module in required_modules:
            if not importlib.util.find_spec(module):
                self.logging.warning(f"Module {module} is not installed.")
                return False
        return True

    def _initialize_provider(self):
        llm_settings = self.config.default_llm_settings
        from llama_cpp_agent.providers import LlamaCppServerProvider
        return LlamaCppServerProvider(
            llm_settings["url"]
        )

    def _initialize_agent(self):
        from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
        from llama_cpp_agent.prompt_templates import web_search_system_prompt
        return LlamaCppAgent(
            self.provider,
            debug_output=True,
            system_prompt=web_search_system_prompt,
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL,
            add_tools_and_structures_documentation_to_system_prompt=True,
        )

    def _initialize_search_tool(self):
        from llama_cpp_agent.tools import WebSearchTool
        return WebSearchTool(
            self.provider,
            MessagesFormatterType.MISTRAL,
            max_tokens_search_results=20000
        )

    def _configure_settings(self):
        self.settings.temperature = 0.65
        self.settings.max_tokens = 2048

    @staticmethod
    def write_message_to_user():
        return "Please write the message to the user."

    def search(self, query):
        if not self.dependencies_available:
            return "Search functionality is disabled due to missing dependencies."

        result = self.agent.get_chat_response(query,
                                              llm_sampling_settings=self.settings,
                                              structured_output_settings=self.output_settings)
        while True:
            if result[0]["function"] == "write_message_to_user":
                break
            else:
                result = self.agent.get_chat_response(result[0]["return_value"], role="tool",
                                                      structured_output_settings=self.output_settings,
                                                      llm_sampling_settings=self.settings)
        result = self.agent.get_chat_response(result[0]["return_value"], role="tool",
                                              llm_sampling_settings=self.settings)
        return result

# Example usage
if __name__ == "__main__":
    config = Config()
    search_module = SearchModule(config)
    while True:
        user_input = input(">")
        if user_input == "exit":
            break
        results = search_module.search(user_input)
        print(f"Search Results: {results}")
