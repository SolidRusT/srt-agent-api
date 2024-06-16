import importlib.util
import sys
import json
from srt_core.config import Config
from srt_core.utils.logger import Logger
from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings, LlmStructuredOutputType
from llama_cpp_agent.providers import VLLMServerProvider, LlamaCppServerProvider, TGIServerProvider
from llama_cpp_agent.rag.rag_colbert_reranker import RAGColbertReranker
from llama_cpp_agent.text_utils import RecursiveCharacterTextSplitter
from ragatouille.utils import get_wikipedia_page
from typing import List
from pydantic import BaseModel, Field


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
            self.output_settings = self._initialize_output_settings()
        else:
            self.logger.info("Wikipedia Query module dependencies are not installed. Disabling functionality.")

    def _check_dependencies(self):
        required_modules = ["llama_cpp_agent", "ragatouille", "chromadb"]
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

    def _initialize_output_settings(self):
        class QueryExtension(BaseModel):
            """
            Represents an extension of a query as additional queries.
            """
            queries: List[str] = Field(default_factory=list, description="List of queries.")

        return LlmStructuredOutputSettings.from_pydantic_models(
            [QueryExtension], LlmStructuredOutputType.object_instance
        )

    def process_wikipedia_query(self, page_url: str, query: str):
        if not self.dependencies_available:
            return "Wikipedia Query functionality is disabled due to missing dependencies."

        # Use the ragatouille helper function to get the content of a Wikipedia page.
        self.logger.debug(f"Retrieving content for page: {page_url}")
        page_content = get_wikipedia_page(page_url)

        if not page_content:
            self.logger.error(f"Failed to retrieve content for page: {page_url}")
            return "Failed to retrieve content for the specified Wikipedia page."

        # Split the text of the Wikipedia page into chunks for the vector database.
        self.logger.debug(f"Splitting content into chunks.")
        splits = self.splitter.split_text(page_content)
        self.logger.debug(f"Total chunks created: {len(splits)}")

        # Add the splits into the vector database
        for split in splits:
            self.rag.add_document(split)
        self.logger.debug(f"Added chunks to the vector database.")

        # Perform the query extension with the agent.
        self.logger.debug(f"Performing query extension.")
        output = self.agent.get_chat_response(
            f"Consider the following query: {query}", structured_output_settings=self.output_settings
        )
        self.logger.debug(f"Query extension output: {output}")

        if not output:
            self.logger.error("No output received from the agent.")
            return "Error: No output received from the agent."

        try:
            # Load the query extension in JSON format and create an instance of the query extension model.
            queries = self.output_settings.models[0].model_validate(json.loads(output))
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON output from the agent: {e}")
            return f"Error decoding JSON output from the agent: {e}"

        self.logger.debug(f"Extended queries: {queries.queries}")

        # Define the final prompt for the query with the retrieved information
        prompt = "Consider the following context:\n==========Context===========\n"

        # Retrieve the most fitting document chunks based on the original query and add them to the prompt.
        documents = self.rag.retrieve_documents(query, k=3)
        for doc in documents:
            prompt += doc["content"] + "\n\n"

        # Retrieve the most fitting document chunks based on the extended queries and add them to the prompt.
        for extended_query in queries.queries:
            documents = self.rag.retrieve_documents(extended_query, k=3)
            for doc in documents:
                if doc["content"] not in prompt:
                    prompt += doc["content"] + "\n\n"

        prompt += "\n======================\nQuestion: " + query

        # Ask the agent the original query with the generated prompt that contains the retrieved information.
        result = self.agent.get_chat_response(prompt)
        return result


# Example usage
if __name__ == "__main__":
    config = Config()
    logger = Logger()
    wikipedia_query_module = WikipediaQueryModule(config, logger)
    page_url = "Synthetic_diamond"
    query = "What is a BARS apparatus?"
    result = wikipedia_query_module.process_wikipedia_query(page_url, query)
    print(f"Query Result: {result}")
