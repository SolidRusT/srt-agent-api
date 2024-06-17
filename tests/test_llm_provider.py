import unittest
from unittest.mock import patch, Mock
from app.modules.llm_provider import LLMProvider
from srt_core.config import Config
from srt_core.utils.logger import Logger

class TestLLMProvider(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.llm_provider = LLMProvider()

    @patch('app.modules.llm_provider.LlamaCppServerProvider')
    def test_initialize_provider_llama_cpp(self, mock_provider):
        mock_instance = mock_provider.return_value
        llm_settings = {
            "agent_provider": "llama_cpp_server",
            "url": "http://localhost:8000"
        }
        provider = self.llm_provider._initialize_provider(llm_settings)
        self.assertEqual(provider, mock_instance)

    @patch('app.modules.llm_provider.VLLMServerProvider')
    def test_initialize_provider_vllm(self, mock_provider):
        mock_instance = mock_provider.return_value
        llm_settings = {
            "agent_provider": "vllm_server",
            "url": "http://localhost:8000",
            "huggingface": "some_model"
        }
        provider = self.llm_provider._initialize_provider(llm_settings)
        self.assertEqual(provider, mock_instance)

    @patch('app.modules.llm_provider.TGIServerProvider')
    def test_initialize_provider_tgi(self, mock_provider):
        mock_instance = mock_provider.return_value
        llm_settings = {
            "agent_provider": "tgi_server",
            "url": "http://localhost:8000"
        }
        provider = self.llm_provider._initialize_provider(llm_settings)
        self.assertEqual(provider, mock_instance)

    @patch('app.modules.llm_provider.GroqProvider')
    def test_initialize_provider_groq(self, mock_provider):
        mock_instance = mock_provider.return_value
        llm_settings = {
            "agent_provider": "groq",
            "url": "https://api.groq.com/openai/v1",
            "model": "mixtral-8x7b-32768",
            "huggingface": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "api_key": "your_api_key"
        }
        provider = self.llm_provider._initialize_provider(llm_settings)
        self.assertEqual(provider, mock_instance)

    @patch('app.modules.llm_provider.LlamaCppPythonProvider')
    @patch('llama_cpp.Llama')
    def test_initialize_provider_llama_cpp_python(self, mock_llama, mock_provider):
        mock_instance = mock_provider.return_value
        mock_llama_instance = mock_llama.return_value
        llm_settings = {
            "agent_provider": "llama_cpp_python",
            "filename": "model_file",
            "max_tokens": 1024
        }
        provider = self.llm_provider._initialize_provider(llm_settings)
        mock_llama.assert_called_with(
            model_path="models/model_file",
            flash_attn=True,
            n_threads=40,
            n_gpu_layers=81,
            n_batch=1024,
            n_ctx=1024
        )
        self.assertEqual(provider, mock_instance)

    @patch('app.modules.llm_provider.LlamaCppServerProvider')
    def test_initialize_provider_llama_cpp_python_server(self, mock_provider):
        mock_instance = mock_provider.return_value
        llm_settings = {
            "agent_provider": "llama_cpp_python_server",
            "url": "http://localhost:8080"
        }
        provider = self.llm_provider._initialize_provider(llm_settings)
        self.assertEqual(provider, mock_instance)

    def test_initialize_provider_invalid(self):
        llm_settings = {
            "agent_provider": "invalid"
        }
        with self.assertRaises(ValueError):
            self.llm_provider._initialize_provider(llm_settings)

if __name__ == '__main__':
    unittest.main()
