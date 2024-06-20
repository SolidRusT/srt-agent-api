from srt_core.config import Config
from srt_core.utils.logger import Logger
from llama_cpp import Llama
import importlib

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
            "model": llm_config.get("model", ""),
            "api_key": llm_config.get("api_key", "")
        }

    def set_llm_attributes(self, llm_prefix, llm_settings):
        for key, value in llm_settings.items():
            setattr(self, f"{llm_prefix}_llm_{key}", value)

    def load_provider_settings(self):
        self.default_llm_settings = self.load_llm_settings(self.config.default_llm_name)
        self.summary_llm_settings = self.load_llm_settings(self.config.summary_llm_name)
        self.chat_llm_settings = self.load_llm_settings(self.config.chat_llm_name)

        self.set_llm_attributes('default', self.default_llm_settings)
        self.set_llm_attributes('summary', self.summary_llm_settings)
        self.set_llm_attributes('chat', self.chat_llm_settings)

        self.default_provider = self._initialize_provider(self.default_llm_settings)
        self.summary_provider = self._initialize_provider(self.summary_llm_settings)
        self.chat_provider = self._initialize_provider(self.chat_llm_settings)

    def _initialize_provider(self, llm_settings):
        self.logger.info(f"Initializing provider with settings: {llm_settings}")
        provider_type = llm_settings["agent_provider"]

        if provider_type == "vllm_server":
            VLLMServerProvider = importlib.import_module("llama_cpp_agent.providers").VLLMServerProvider
            return VLLMServerProvider(
                llm_settings["url"],
                llm_settings["huggingface"],
                llm_settings["huggingface"],
                llm_settings.get("api_key", self.config.openai_compatible_api_key)
            )
        elif provider_type == "llama_cpp_server":
            LlamaCppServerProvider = importlib.import_module("llama_cpp_agent.providers").LlamaCppServerProvider
            return LlamaCppServerProvider(llm_settings["url"])
        elif provider_type == "tgi_server":
            TGIServerProvider = importlib.import_module("llama_cpp_agent.providers").TGIServerProvider
            return TGIServerProvider(server_address=llm_settings["url"])
        elif provider_type == "llama_cpp_python":
            LlamaCppPythonProvider = importlib.import_module("llama_cpp_agent.providers").LlamaCppPythonProvider
            llama_model = Llama(
                model_path=f"models/{llm_settings['filename']}",
                flash_attn=True,
                n_threads=40,
                n_gpu_layers=81,
                n_batch=1024,
                n_ctx=llm_settings["max_tokens"],
            )
            return LlamaCppPythonProvider(llama_model)
        elif provider_type == "groq":
            GroqProvider = importlib.import_module("llama_cpp_agent.providers").GroqProvider
            return GroqProvider(
                base_url=llm_settings["url"],
                model=llm_settings["model"],
                huggingface_model=llm_settings["huggingface"],
                api_key=llm_settings["api_key"]
            )
        elif provider_type == "llama_cpp_python_server":
            LlamaCppServerProvider = importlib.import_module("llama_cpp_agent.providers").LlamaCppServerProvider
            return LlamaCppServerProvider(llm_settings["url"], llama_cpp_python_server=True)
        else:
            self.logger.error(f"Unsupported provider: {provider_type}")
            raise ValueError(f"Unsupported provider: {provider_type}")

# Example usage
if __name__ == "__main__":
    provider = LLMProvider()
    print(provider.default_provider)
    print(provider.summary_provider)
    print(provider.chat_provider)
