import unittest
import json
from unittest.mock import patch, Mock
from app.modules.wikipedia_query_module import WikipediaQueryModule
from srt_core.config import Config
from srt_core.utils.logger import Logger

class TestWikipediaQueryModule(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.wikipedia_query_module = WikipediaQueryModule(self.config, self.logger)

    @patch('ragatouille.utils.get_wikipedia_page')
    @patch('llama_cpp_agent.LlamaCppAgent.get_chat_response')
    def test_process_wikipedia_query_success(self, mock_get_chat_response, mock_get_wikipedia_page):
        mock_get_wikipedia_page.return_value = "Test page content"
        mock_get_chat_response.return_value = json.dumps({"queries": ["Test query 1", "Test query 2"]})

        result = self.wikipedia_query_module.process_wikipedia_query("https://en.wikipedia.org/wiki/Synthetic_diamond", "What is a BARS apparatus?")
        self.assertIsNotNone(result)
        self.assertIn("result", result)

    @patch('ragatouille.utils.get_wikipedia_page')
    @patch('llama_cpp_agent.LlamaCppAgent.get_chat_response')
    def test_process_wikipedia_query_failure(self, mock_get_chat_response, mock_get_wikipedia_page):
        mock_get_wikipedia_page.side_effect = Exception("Error fetching Wikipedia page")
        mock_get_chat_response.side_effect = Exception("Error processing query")

        result = self.wikipedia_query_module.process_wikipedia_query("https://en.wikipedia.org/wiki/Synthetic_diamond", "What is a BARS apparatus?")
        self.assertIn("error", result)

if __name__ == '__main__':
    unittest.main()
