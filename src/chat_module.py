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
        default_agent_name = self.config.persona_full_name
        default_system_prompt = self.config.persona_system_message
        default_persona = self.config.persona_prompt_message
        default_prompt = default_system_prompt + "\nMy name is " + default_agent_name + ".\n" + default_persona + "\n"
        return LlamaCppAgent(
            self.provider,
            system_prompt=default_prompt,
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL,
        )

    def _configure_settings(self):
        self.settings.max_tokens = 512
        self.settings.temperature = 0.65

    def chat(self, prompt):
        response = self.agent.get_chat_response(prompt, llm_sampling_settings=self.settings)
        return response.strip()
