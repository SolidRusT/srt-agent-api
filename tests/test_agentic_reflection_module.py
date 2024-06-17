import unittest
from unittest.mock import patch, MagicMock
from app.modules.agentic_reflection_module import AgenticReflectionModule
from srt_core.config import Config
from srt_core.utils.logger import Logger

class TestAgenticReflectionModule(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.agentic_reflection_module = AgenticReflectionModule(self.config, self.logger)

    @patch('app.modules.agentic_reflection_module.LlamaCppAgent')
    def test_get_reflective_response(self, mock_agent):
        mock_agent_instance = mock_agent.return_value
        mock_agent_instance.get_chat_response.return_value = '{"response_state": "approved"}'
        mock_agent_instance.chat_history.get_latest_message.return_value = MagicMock(content="Approved response")

        response = self.agentic_reflection_module.get_reflective_response("Test input")
        self.assertEqual(response, "Approved response")

if __name__ == '__main__':
    unittest.main()
