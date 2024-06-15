import sys
import importlib.util
from srt_core.config import Config
from srt_core.utils.logger import Logger
from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType

class WikiSummaryModule:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.dependencies_available = self._check_dependencies()

        if self.dependencies_available:
            self.agent = self._initialize_agent()
            self.search_tool = self._initialize_search_tool()
            self.settings = self._configure_settings()
        else:
            self.logger.info("WikiSummary module dependencies are not installed. Disabling functionality.")

    def _check_dependencies(self):
        required_modules = ["ragatouille", "pydantic", "typing"]
        missing_modules = []
        for module in required_modules:
            if not importlib.util.find_spec(module):
                self.logger.warning(f"Module {module} is not installed.")
                missing_modules.append(module)
        if missing_modules:
            self.logger.error(f"Missing required modules: {', '.join(missing_modules)}")
            return False
        return True

    def _initialize_agent(self):
        from ragatouille.utils import get_wikipedia_page
        from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings, LlmStructuredOutputType
        from llama_cpp_agent.messages_formatter import MessagesFormatterType
        from llama_cpp_agent.providers import LlamaCppServerProvider

        model = LlamaCppServerProvider(self.config.default_llm_settings["url"])
        agent = LlamaCppAgent(
            model,
            debug_output=True,
            system_prompt="You are a world-class AI assistant.",
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL
        )
        return agent

    def _initialize_search_tool(self):
        from llama_cpp_agent.tools import WebSearchTool
        return WebSearchTool(
            self.agent.provider,
            MessagesFormatterType.MISTRAL,
            max_tokens_search_results=20000
        )

    def _configure_settings(self):
        settings = self.agent.provider.get_provider_default_settings()
        settings.temperature = 0.65
        settings.max_tokens = 2048
        return settings

    def summarize_wikipedia_page(self, title):
        if not self.dependencies_available:
            return "WikiSummary functionality is disabled due to missing dependencies."

        from ragatouille.utils import get_wikipedia_page
        from ragatouille.rag.rag_colbert_reranker import RAGColbertReranker
        from ragatouille.text_utils import RecursiveCharacterTextSplitter

        rag = RAGColbertReranker(persistent=False)
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=512,
            chunk_overlap=0,
            length_function=len,
            keep_separator=True
        )

        page = get_wikipedia_page(title)
        splits = splitter.split_text(page)

        for split in splits:
            rag.add_document(split)

        query = f"Summarize the Wikipedia page for {title}"
        documents = rag.retrieve_documents(query, k=3)

        prompt = "Consider the following context:\n==========Context===========\n"
        for doc in documents:
            prompt += doc["content"] + "\n\n"
        prompt += "\n======================\nQuestion: " + query

        response = self.agent.get_chat_response(prompt, llm_sampling_settings=self.settings)
        return response.strip()

# Example usage
if __name__ == "__main__":
    config = Config()
    logger = Logger()
    wiki_summary_module = WikiSummaryModule(config, logger)
    while True:
        user_input = input(">")
        if user_input == "exit":
            break
        summary = wiki_summary_module.summarize_wikipedia_page(user_input)
        print(f"Summary: {summary}")
