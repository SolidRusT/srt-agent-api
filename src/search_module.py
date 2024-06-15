import sys
import importlib.util
from srt_core.config import Config
from srt_core.utils.logger import Logger
from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings
from llama_cpp_agent.prompt_templates import web_search_system_prompt
from llama_cpp_agent.providers import VLLMServerProvider, LlamaCppServerProvider, TGIServerProvider
from llama_cpp_agent.tools import WebSearchTool

class SearchModule:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.dependencies_available = self._check_dependencies()
        
        if self.dependencies_available:
            self.provider = self._initialize_provider()
            self.agent = self._initialize_agent()
            self.search_tool = self._initialize_search_tool()
            self.settings = self.provider.get_provider_default_settings()
            self._configure_settings()
            try:
                self.output_settings = LlmStructuredOutputSettings.from_functions(
                    [self.search_tool.get_tool(), self.write_message_to_user]
                )
            except AssertionError as e:
                self.logger.error(f"Error creating structured output settings: {e}")
                raise
        else:
            self.logger.info("Search tool dependencies are not installed. Disabling search functionality.")

    def _check_dependencies(self):
        self.logger.info(f"Python executable: {sys.executable}")
        self.logger.info(f"sys.path: {sys.path}")
        required_modules = ["llama_cpp_agent", "readability-lxml", "trafilatura"]
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                self.logger.warning(f"Module {module} is not installed.")
                missing_modules.append(module)
        if missing_modules:
            self.logger.error(f"Missing required modules: {', '.join(missing_modules)}")
            return False
        return True

    def _initialize_provider(self):
        llm_settings = self.config.default_llm_settings
        if llm_settings["agent_provider"] == "vllm_server":
            return VLLMServerProvider(
                llm_settings["url"],
                llm_settings["huggingface"],
                llm_settings["huggingface"],
                self.config.openai_compatible_api_key,
            )
        elif llm_settings["agent_provider"] == "llama_cpp_server":
            return LlamaCppServerProvider(llm_settings["url"])
        elif llm_settings["agent_provider"] == "tgi_server":
            return TGIServerProvider(server_address=llm_settings["url"])
        else:
            self.logger.error(f"Unsupported provider: {llm_settings['agent_provider']}")
            raise ValueError(f"Unsupported provider: {llm_settings['agent_provider']}")

    def _initialize_agent(self):
        return LlamaCppAgent(
            self.provider,
            debug_output=True,
            system_prompt=web_search_system_prompt,
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL,
            add_tools_and_structures_documentation_to_system_prompt=True,
        )

    def _initialize_search_tool(self):
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
        """
        This function simulates writing a message to the user.
        """
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
    logger = Logger()
    search_module = SearchModule(config, logger)
    while True:
        user_input = input(">")
        if user_input == "exit":
            break
        results = search_module.search(user_input)
        print(f"Search Results: {results}")
