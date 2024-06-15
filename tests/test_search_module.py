import unittest
from unittest.mock import patch, Mock
from app.modules.search_module import SearchModule
from srt_core.config import Config
from srt_core.utils.logger import Logger

class TestSearchModule(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.search_module = SearchModule(self.config, self.logger)

    @patch('app.modules.search_module.LlamaCppServerProvider')
    def test_initialize_provider_llama_cpp(self, mock_provider):
        mock_instance = mock_provider.return_value
        self.search_module.config.default_llm_settings["agent_provider"] = "llama_cpp_server"
        provider = self.search_module._initialize_provider()
        self.assertEqual(provider, mock_instance)

    @patch('app.modules.search_module.VLLMServerProvider')
    def test_initialize_provider_vllm(self, mock_provider):
        mock_instance = mock_provider.return_value
        self.search_module.config.default_llm_settings["agent_provider"] = "vllm_server"
        provider = self.search_module._initialize_provider()
        self.assertEqual(provider, mock_instance)

    @patch('app.modules.search_module.TGIServerProvider')
    def test_initialize_provider_tgi(self, mock_provider):
        mock_instance = mock_provider.return_value
        self.search_module.config.default_llm_settings["agent_provider"] = "tgi_server"
        provider = self.search_module._initialize_provider()
        self.assertEqual(provider, mock_instance)

    def test_initialize_provider_invalid(self):
        self.search_module.config.default_llm_settings["agent_provider"] = "invalid"
        with self.assertRaises(ValueError):
            self.search_module._initialize_provider()

if __name__ == '__main__':
    unittest.main()
