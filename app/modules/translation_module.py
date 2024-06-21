from llama_cpp_agent import LlamaCppAgent
from llama_cpp_agent.providers import LlamaCppServerProvider
from llama_cpp_agent.llm_output_settings import MessagesFormatterType
from app.modules.base_module import BaseModule

class TranslationModule(BaseModule):
    def __init__(self, config, logger):
        super().__init__(config, logger, ["llama_cpp_agent"])
        if self.dependencies_available:
            self.provider = self._initialize_provider()
            self.agent = self._initialize_agent(
                system_prompt="You are a highly skilled translator. Your task is to translate text from one language to another.",
                predefined_messages_formatter_type=MessagesFormatterType.MISTRAL
            )

    def translate(self, text, source_language, target_language):
        prompt = f"Translate the following text from {source_language} to {target_language}:\n\n{text}"
        self.logger.debug(f"Translating text: {text} from {source_language} to {target_language}")
        response = self.agent.get_chat_response(prompt)
        self.logger.debug(f"Translation result: {response.strip()}")
        return response.strip()
