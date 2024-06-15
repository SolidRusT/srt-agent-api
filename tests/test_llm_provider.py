import unittest
from unittest.mock import patch, Mock
from app.modules.llm_provider import LLMProvider
from srt_core.config import Config
from srt_core.utils.logger import Logger

class TestLLMProvider(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.llm_provider = LLMProvider(self.config, self.logger)

    @patch('app.modules.llm_provider.LlamaCppServerProvider')
    def test_initialize_provider_llama_cpp(self, mock_provider):
        mock_instance = mock_provider.return_value
        provider = self.llm_provider._initialize_provider("llama_cpp")
        self.assertEqual(provider, mock_instance)

    @patch('app.modules.llm_provider.VLLMServerProvider')
    def test_initialize_provider_vllm(self, mock_provider):
        mock_instance = mock_provider.return_value
        provider = self.llm_provider._initialize_provider("vllm")
        self.assertEqual(provider, mock_instance)

    def test_initialize_provider_invalid(self):
        with self.assertRaises(ValueError):
            self.llm_provider._initialize_provider("invalid")

if __name__ == '__main__':
    unittest.main()
