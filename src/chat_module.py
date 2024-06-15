from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.providers import VLLMServerProvider

class ChatModule:
    def __init__(self, config, logger):
        self.config = config
        self.provider = self._initialize_provider()
        self.agent = self._initialize_agent()
        self.settings = self.provider.get_provider_default_settings()
        self._configure_settings()

    def _initialize_provider(self):
        llm_settings = self.config.default_llm_settings
        return VLLMServerProvider(
            llm_settings["url"],
            llm_settings["huggingface"],
            llm_settings["huggingface"],
            self.config.openai_compatible_api_key
        )

    def _initialize_agent(self):
        return LlamaCppAgent(
            self.provider,
            system_prompt="You are a helpful assistant.",
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL,
        )

    def _configure_settings(self):
        self.settings.max_tokens = 512
        self.settings.temperature = 0.65

    def chat(self, prompt):
        response = self.agent.get_chat_response(prompt, llm_sampling_settings=self.settings)
        return response.strip()
