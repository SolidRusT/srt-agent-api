import json
from pydantic import BaseModel, Field
from typing import List
from ragatouille.utils import get_wikipedia_page
from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings, LlmStructuredOutputType
from llama_cpp_agent.messages_formatter import MessagesFormatterType
from llama_cpp_agent.llm_agent import LlamaCppAgent
from llama_cpp_agent.rag.rag_colbert_reranker import RAGColbertReranker
from llama_cpp_agent.text_utils import RecursiveCharacterTextSplitter
from llama_cpp_agent.providers import LlamaCppServerProvider, VLLMServerProvider, TGIServerProvider
from srt_core.config import Config
from srt_core.utils.logger import Logger

class WikipediaQueryModule:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.dependencies_available = self._check_dependencies()
        
        if self.dependencies_available:
            self.rag = RAGColbertReranker(persistent=False)
            self.provider = self._initialize_provider()
            self.agent = self._initialize_agent()
            self.splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", " ", ""],
                chunk_size=512,
                chunk_overlap=0,
                length_function=len,
                keep_separator=True
            )
        else:
            self.logger.info("Wikipedia Query module dependencies are not installed. Disabling functionality.")
    
    def _check_dependencies(self):
        required_modules = ["llama_cpp_agent", "ragatouille"]
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
        self.logger.info(f"Initializing provider with settings: {llm_settings}")
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
        self.logger.info("Initializing LlamaCppAgent.")
        return LlamaCppAgent(
            self.provider,
            debug_output=True,
            system_prompt="You are an advanced AI assistant, trained by OpenAI.",
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL,
        )

    def process_wikipedia_query(self, page_url: str, query: str):
        try:
            page_content = get_wikipedia_page(page_url)
            splits = self.splitter.split_text(page_content)

            for split in splits:
                self.rag.add_document(split)

            class QueryExtension(BaseModel):
                queries: List[str] = Field(default_factory=list, description="List of queries.")

            output_settings = LlmStructuredOutputSettings.from_pydantic_models([QueryExtension], LlmStructuredOutputType.object_instance)

            query_extension_agent = LlamaCppAgent(
                self.provider,
                debug_output=True,
                system_prompt="You are a world class query extension algorithm capable of extending queries by writing new queries. Do not answer the queries, simply provide a list of additional queries in JSON format.",
                predefined_messages_formatter_type=MessagesFormatterType.MISTRAL
            )

            output = query_extension_agent.get_chat_response(
                f"Consider the following query: {query}", structured_output_settings=output_settings)

            queries = QueryExtension.model_validate(json.loads(output))

            prompt = "Consider the following context:\n==========Context===========\n"

            documents = self.rag.retrieve_documents(query, k=3)
            for doc in documents:
                prompt += doc["content"] + "\n\n"

            for qu in queries.queries:
                documents = self.rag.retrieve_documents(qu, k=3)
                for doc in documents:
                    if doc["content"] not in prompt:
                        prompt += doc["content"] + "\n\n"
            prompt += "\n======================\nQuestion: " + query

            agent_with_rag_information = LlamaCppAgent(
                self.provider,
                debug_output=True,
                system_prompt="You are an advanced AI assistant, trained by OpenAI. Only answer questions based on the context information provided.",
                predefined_messages_formatter_type=MessagesFormatterType.MISTRAL
            )

            result = agent_with_rag_information.get_chat_response(prompt)
            return result

        except Exception as e:
            self.logger.error(f"Error processing Wikipedia query: {e}")
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    config = Config()
    logger = Logger()
    wikipedia_query_module = WikipediaQueryModule(config, logger)
    page_url = "https://en.wikipedia.org/wiki/Synthetic_diamond"
    query = "What is a BARS apparatus?"
    results = wikipedia_query_module.process_wikipedia_query(page_url, query)
    print(f"Query Results: {results}")
