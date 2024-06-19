from llama_cpp_agent.tools import WebSearchTool
from llama_cpp_agent import MessagesFormatterType
from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings
from app.modules.base_module import BaseModule


class SearchModule(BaseModule):
    def __init__(self, config, logger):
        required_modules = ["llama_cpp_agent", "readability", "trafilatura"]
        super().__init__(config, logger, required_modules)

        if self.dependencies_available:
            self.provider = self._initialize_provider(config.default_llm_settings)
            self.agent = self._initialize_agent("You are a web search assistant.")
            self.search_tool = WebSearchTool(
                self.provider,
                MessagesFormatterType.MISTRAL,
                max_tokens_search_results=20000
            )
            self.settings = self.provider.get_provider_default_settings()
            self._configure_settings()
            self.output_settings = LlmStructuredOutputSettings.from_functions(
                [self.search_tool.get_tool(), self.write_message_to_user])
        else:
            self.logger.info("Search tool dependencies are not installed. Disabling search functionality.")

    def _configure_settings(self):
        self.logger.info("Configuring settings.")
        self.settings.temperature = 0.65
        self.settings.max_tokens = 2048

    @staticmethod
    def write_message_to_user():
        """
        Write message back to the user.
        """
        return "Please write the message to the user."

    def search(self, query):
        if not self.dependencies_available or not self.search_tool or not self.output_settings:
            return "Search functionality is disabled due to missing dependencies."

        result = self.agent.get_chat_response(query, llm_sampling_settings=self.settings,
                                              structured_output_settings=self.output_settings)
        return result
