import unittest
from unittest.mock import patch, Mock
from app.modules.chat_module import ChatModule
from srt_core.config import Config
from srt_core.utils.logger import Logger

class TestChatModule(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.chat_module = ChatModule(self.config, self.logger)

    @patch('app.modules.chat_module.LlamaCppAgent.get_chat_response')
    def test_chat_success(self, mock_get_chat_response):
        mock_get_chat_response.return_value = "Hello, how can I help you?"
        response = self.chat_module.chat("Hi")
        self.assertEqual(response, "Hello, how can I help you?")

    @patch('app.modules.chat_module.LlamaCppAgent.get_chat_response')
    def test_chat_failure(self, mock_get_chat_response):
        mock_get_chat_response.side_effect = Exception("Error")
        response = self.chat_module.chat("Hi")
        self.assertIn("Error", response)

if __name__ == '__main__':
    unittest.main()
