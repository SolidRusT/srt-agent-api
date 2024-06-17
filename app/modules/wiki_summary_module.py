from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings, LlmStructuredOutputType
from ragatouille.utils import get_wikipedia_page
from app.modules.base_module import BaseModule
from llama_cpp_agent.text_utils import RecursiveCharacterTextSplitter

class WikiSummaryModule(BaseModule):
    def __init__(self, config, logger):
        required_modules = ["llama_cpp_agent", "ragatouille"]
        super().__init__(config, logger, required_modules)

        if self.dependencies_available:
            self.provider = self._initialize_provider()
            self.agent = self._initialize_agent("You are an advanced AI assistant, trained by OpenAI.")
            self.splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", " ", ""],
                chunk_size=512,
                chunk_overlap=0,
                length_function=len,
                keep_separator=True
            )
        else:
            self.logger.info("WikiSummary module dependencies are not installed. Disabling functionality.")

    def summarize_wikipedia_page(self, page_title):
        if not self.dependencies_available:
            return "WikiSummary functionality is disabled due to missing dependencies."

        try:
            page_content = get_wikipedia_page(page_title)
            splits = self.splitter.split_text(page_content)
            summary = self.agent.get_chat_response(
                f"Summarize the following text:\n\n{splits}",
                structured_output_settings=LlmStructuredOutputSettings.from_functions([self.write_message_to_user])
            )
            return summary
        except Exception as e:
            self.logger.error(f"Error summarizing Wikipedia page {page_title}: {e}")
            raise ValueError(f"Error summarizing Wikipedia page: {e}")

    @staticmethod
    def write_message_to_user():
        return "Please write the message to the user."
