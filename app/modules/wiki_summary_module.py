import json
from ragatouille.utils import get_wikipedia_page
from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.providers import LlamaCppServerProvider, VLLMServerProvider
from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings
from llama_cpp_agent.tools import WebSearchTool
from srt_core.config import Config
from srt_core.utils.logger import Logger
from pydantic import BaseModel, Field
from typing import List

class WikiSummaryModule:
    def __init__(self, config: Config, logger: Logger):
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
            self.logger.info("WikiSummary tool dependencies are not installed. Disabling functionality.")

    def _check_dependencies(self):
        try:
            import ragatouille
            import typing_extensions
            return True
        except ImportError as e:
            self.logger.error(f"Missing dependency: {e}")
            return False

    def _initialize_provider(self):
        llm_settings = self.config.default_llm_settings
        if llm_settings["agent_provider"] == "llama_cpp_server":
            return LlamaCppServerProvider(llm_settings["url"])
        elif llm_settings["agent_provider"] == "vllm_server":
            return VLLMServerProvider(
                llm_settings["url"],
                llm_settings["huggingface"],
                llm_settings["huggingface"],
                self.config.openai_compatible_api_key
            )
        else:
            self.logger.error(f"Unsupported provider: {llm_settings['agent_provider']}")
            raise ValueError(f"Unsupported provider: {llm_settings['agent_provider']}")

    def _initialize_agent(self):
        return LlamaCppAgent(
            self.provider,
            debug_output=True,
            system_prompt="You are an advanced AI assistant, trained by OpenAI.",
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL
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
        Write a message to the user.
        """
        return "Please write the message to the user."

    def summarize_wikipedia_page(self, title: str):
        if not self.dependencies_available:
            return "WikiSummary functionality is disabled due to missing dependencies."

        query = f"Summarize the Wikipedia page for {title}"
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
    wiki_summary_module = WikiSummaryModule(config, logger)
    print(wiki_summary_module.summarize_wikipedia_page("Python (programming language)"))
