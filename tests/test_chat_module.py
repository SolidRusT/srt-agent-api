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

    @patch('app.modules.chat_module.FunctionCallingAgent')
    def test_chat_function_calling(self, mock_agent):
        mock_agent_instance = mock_agent.return_value
        mock_agent_instance.generate_response.return_value = "Current datetime is 2023-11-24 15:42:35"
        response = self.chat_module.chat("What is the current date and time?")
        self.assertEqual(response, "Current datetime is 2023-11-24 15:42:35")

if __name__ == '__main__':
    unittest.main()
