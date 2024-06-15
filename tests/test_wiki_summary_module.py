import unittest
from unittest.mock import patch, Mock
from app.modules.wiki_summary_module import WikiSummaryModule
from srt_core.config import Config
from srt_core.utils.logger import Logger

class TestWikiSummaryModule(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.wiki_summary_module = WikiSummaryModule(self.config, self.logger)

    @patch('app.modules.wiki_summary_module.get_wikipedia_page')
    @patch('app.modules.wiki_summary_module.LlamaCppAgent')
    @patch('app.modules.wiki_summary_module.LlamaCppServerProvider')
    def test_summarize_wikipedia_page(self, mock_provider, mock_agent, mock_get_page):
        mock_provider_instance = mock_provider.return_value
        mock_agent_instance = mock_agent.return_value
        mock_get_page.return_value = "Sample Wikipedia page content."

        self.wiki_summary_module.provider = mock_provider_instance
        self.wiki_summary_module.agent = mock_agent_instance

        response_mock = Mock()
        response_mock.get_chat_response.return_value = "This is a summary."

        mock_agent_instance.get_chat_response = response_mock.get_chat_response

        summary = self.wiki_summary_module.summarize_wikipedia_page("Sample_Title")
        self.assertEqual(summary, "This is a summary.")
        mock_get_page.assert_called_once_with("Sample_Title")

if __name__ == '__main__':
    unittest.main()
