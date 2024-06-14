from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.providers import VLLMServerProvider

class ChatModule:
    def __init__(self, config):
        provider = VLLMServerProvider(
            config.default_llm_settings["url"], 
            config.default_llm_settings["filename"], 
            config.default_llm_settings["huggingface"], 
            config.openai_compatible_api_key
        )
        self.agent = LlamaCppAgent(
            provider,
            system_prompt="You are a helpful assistant.",
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL,
        )
        self.settings = provider.get_provider_default_settings()
        self.settings.max_tokens = 512
        self.settings.temperature = 0.65

    def chat(self, prompt):
        response = self.agent.get_chat_response(prompt, llm_sampling_settings=self.settings)
        return response.strip()
