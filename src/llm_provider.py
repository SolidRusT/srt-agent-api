import os
from srt_core.config import Config
from srt_core.utils.logger import Logger

class LLMProvider:
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.load_provider_settings()

    def load_llm_settings(self, llm_name):
        llm_config = self.config.config["llms"][llm_name]
        return {
            "type": llm_config["type"],
            "filename": llm_config["filename"],
            "huggingface": llm_config["huggingface"],
            "url": llm_config["url"],
            "agent_provider": llm_config["agent_provider"],
            "server_name": llm_config["server"],
            "max_tokens": llm_config["max_tokens"],
        }

    def set_llm_attributes(self, llm_prefix, llm_settings):
        setattr(self, f"{llm_prefix}_llm_type", llm_settings["type"])
        setattr(self, f"{llm_prefix}_llm_filename", llm_settings["filename"])
        setattr(self, f"{llm_prefix}_llm_huggingface", llm_settings["huggingface"])
        setattr(self, f"{llm_prefix}_llm_url", llm_settings["url"])
        setattr(self, f"{llm_prefix}_llm_agent_provider", llm_settings["agent_provider"])
        setattr(self, f"{llm_prefix}_llm_server_name", llm_settings["server_name"])
        setattr(self, f"{llm_prefix}_llm_max_tokens", llm_settings["max_tokens"])

    def load_provider_settings(self):
        self.default_llm_settings = self.load_llm_settings(self.config.default_llm_name)
        self.summary_llm_settings = self.load_llm_settings(self.config.summary_llm_name)
        self.chat_llm_settings = self.load_llm_settings(self.config.chat_llm_name)

        self.set_llm_attributes('default', self.default_llm_settings)
        self.set_llm_attributes('summary', self.summary_llm_settings)
        self.set_llm_attributes('chat', self.chat_llm_settings)

        if "llama_cpp_server" in self.default_llm_settings["agent_provider"]:
            from llama_cpp_agent.providers import LlamaCppServerProvider
            self.default_provider = LlamaCppServerProvider(self.default_llm_settings["url"])
            self.summary_provider = LlamaCppServerProvider(self.summary_llm_settings["url"])
            self.chat_provider = LlamaCppServerProvider(self.chat_llm_settings["url"])
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
            self.logger.error(f"Unsupported llama-cpp-agent provider: {self.default_llm_settings['agent_provider']}, {self.summary_llm_settings['agent_provider']}, {self.chat_llm_settings['agent_provider']}")

# Example usage
if __name__ == "__main__":
    provider = LLMProvider()
    print(provider.default_provider)
    print(provider.summary_provider)
    print(provider.chat_provider)
