from llama_cpp_agent import WebSearchAgent
from srt_core.config import Config

class SearchModule:
    def __init__(self, config):
        self.config = config
        self.agent = WebSearchAgent(api_key=config.openai_compatible_api_key)

    def search(self, query):
        results = self.agent.search(query)
        return results
