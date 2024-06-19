from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings, LlmStructuredOutputType
from llama_cpp_agent.rag.rag_colbert_reranker import RAGColbertReranker
from llama_cpp_agent.text_utils import RecursiveCharacterTextSplitter
from ragatouille.utils import get_wikipedia_page
from pydantic import BaseModel, Field
from typing import List
from app.modules.base_module import BaseModule

class WikipediaQueryModule(BaseModule):
    def __init__(self, config, logger):
        required_modules = ["llama_cpp_agent", "ragatouille", "chromadb"]
        super().__init__(config, logger, required_modules)

        if self.dependencies_available:
            self.provider = self._initialize_provider(config.default_llm_settings)
            self.agent = self._initialize_agent("You are an advanced AI assistant, trained by OpenAI.")
            self.rag = RAGColbertReranker(persistent=False)
            self.splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", " ", ""],
                chunk_size=512,
                chunk_overlap=0,
                length_function=len,
                keep_separator=True
            )
        else:
            self.logger.info("Wikipedia Query module dependencies are not installed. Disabling functionality.")

    def process_wikipedia_query(self, page_url, query):
        try:
            page_content = get_wikipedia_page(page_url)
            splits = self.splitter.split_text(page_content)
            for split in splits:
                self.rag.add_document(split)

            output_settings = LlmStructuredOutputSettings.from_functions([self.write_message_to_user])
            result = self.agent.get_chat_response(query, structured_output_settings=output_settings)
            return result
        except Exception as e:
            self.logger.error(f"Error processing Wikipedia query for page: {page_url} and query: {query}, error: {e}")
            raise ValueError(f"Error processing Wikipedia query: {e}")

    @staticmethod
    def write_message_to_user():
        return "Please write the message to the user."
