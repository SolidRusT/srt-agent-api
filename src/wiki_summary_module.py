import json
from typing import List
from pydantic import BaseModel, Field
from ragatouille.utils import get_wikipedia_page
from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings, LlmStructuredOutputType
from llama_cpp_agent.providers import VLLMServerProvider, LlamaCppServerProvider, TGIServerProvider
from llama_cpp_agent.text_utils import RecursiveCharacterTextSplitter
from llama_cpp_agent.rag.rag_colbert_reranker import RAGColbertReranker
from srt_core.config import Config
from srt_core.utils.logger import Logger

class QueryExtension(BaseModel):
    queries: List[str] = Field(default_factory=list, description="List of queries.")

class WikiSummaryModule:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.provider = self._initialize_provider()
        self.agent = self._initialize_agent()
        self.rag = RAGColbertReranker(persistent=False)
        self.splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=512,
            chunk_overlap=0,
            length_function=len,
            keep_separator=True
        )

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
            system_prompt="You are an advanced AI assistant, trained by OpenAI.",
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL,
        )

    def summarize_wikipedia_page(self, page_title):
        page_content = get_wikipedia_page(page_title)
        if not page_content:
            return f"Could not retrieve Wikipedia page for '{page_title}'."

        splits = self.splitter.split_text(page_content)
        for split in splits:
            self.rag.add_document(split)

        query = f"Summarize the Wikipedia page for {page_title}."
        documents = self.rag.retrieve_documents(query, k=3)
        prompt = "Consider the following context:\n==========Context===========\n"
        for doc in documents:
            prompt += doc["content"] + "\n\n"
        prompt += "\n======================\nQuestion: " + query

        result = self.agent.get_chat_response(prompt)
        return result.strip()

# Example usage
if __name__ == "__main__":
    config = Config()
    logger = Logger()
    wiki_summary_module = WikiSummaryModule(config, logger)
    summary = wiki_summary_module.summarize_wikipedia_page("Synthetic diamond")
    print(f"Summary: {summary}")
