import os
import yaml

# Provider specific settings for default LLM
class Provider:
    def __init__(self):
        # Load configuration from yaml file
        with open("config.yaml", "r") as stream:
            self.config = yaml.safe_load(stream)

def load_provider_settings(self):
        self.default_llm_settings = self.load_llm_settings(self.default_llm_name)
        self.summary_llm_settings = self.load_llm_settings(self.summary_llm_name)
        self.chat_llm_settings = self.load_llm_settings(self.chat_llm_name)

        self.set_llm_attributes('default', self.default_llm_settings)
        self.set_llm_attributes('summary', self.summary_llm_settings)
        self.set_llm_attributes('chat', self.chat_llm_settings)

        # Provider specific settings for default LLM
        if "llama_cpp_server" in self.default_llm_settings["agent_provider"]:
            from llama_cpp_agent.providers import LlamaCppServerProvider
            self.default_provider = LlamaCppServerProvider(self.default_llm_settings["url"])
            self.default_summary = LlamaCppServerProvider(self.summary_llm_settings["url"])
            self.default_chat = LlamaCppServerProvider(self.chat_llm_settings["url"])
        elif "llama_cpp_python" in self.default_llm_settings["agent_provider"]:
            from llama_cpp import Llama
            from llama_cpp_agent.providers import LlamaCppPythonProvider
            python_cpp_llm = Llama(
                model_path=f"models/{self.default_llm_settings['filename']}",
                flash_attn=True,
                n_threads=40,
                n_gpu_layers=81,
                n_batch=1024,
                n_ctx=self.default_llm_settings["max_tokens"],
            )
            self.default_provider = LlamaCppPythonProvider(python_cpp_llm)
            self.summary_provider = LlamaCppPythonProvider(python_cpp_llm)
            self.chat_provider = LlamaCppPythonProvider(python_cpp_llm)
        elif "tgi_server" in self.default_llm_settings["agent_provider"]:
            from llama_cpp_agent.providers import TGIServerProvider
            self.default_provider = TGIServerProvider(server_address=self.default_llm_settings["url"])
            self.summary_provider = TGIServerProvider(server_address=self.summary_llm_settings["url"])
            self.chat_provider = TGIServerProvider(server_address=self.chat_llm_settings["url"])
        elif "vllm_server" in self.default_llm_settings["agent_provider"]:
            from llama_cpp_agent.providers import VLLMServerProvider
            self.default_provider = VLLMServerProvider(
                base_url=self.default_llm_settings["url"],
                model=self.default_llm_settings["huggingface"],
                huggingface_model=self.default_llm_settings["huggingface"],
            )
            self.summary_provider = VLLMServerProvider(
                base_url=self.summary_llm_settings["url"],
                model=self.summary_llm_settings["huggingface"],
                huggingface_model=self.summary_llm_settings["huggingface"],
            )
            self.chat_provider = VLLMServerProvider(
                base_url=self.chat_llm_settings["url"],
                model=self.chat_llm_settings["huggingface"],
                huggingface_model=self.chat_llm_settings["huggingface"],
            )
        else:
            return (
                "unsupported llama-cpp-agent provider:",
                self.default_llm_settings["agent_provider"],
                self.summary_llm_settings["agent_provider"],
                self.chat_llm_settings["agent_provider"],
            )