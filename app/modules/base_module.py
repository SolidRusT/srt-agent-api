from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.providers import (
    LlamaCppServerProvider,
    VLLMServerProvider,
    TGIServerProvider,
    LlamaCppPythonProvider,
    #GroqProvider
)
from llama_cpp import Llama

class BaseModule:
    def __init__(self, config, logger, required_modules):
        self.config = config
        self.logger = logger
        self.required_modules = required_modules
        self.dependencies_available = self._check_dependencies()

    def _check_dependencies(self):
        missing_modules = []
        for module in self.required_modules:
            try:
                __import__(module)
            except ImportError:
                self.logger.warning(f"Module {module} is not installed.")
                missing_modules.append(module)
        if missing_modules:
            self.logger.error(f"Missing required modules: {', '.join(missing_modules)}")
            return False
        return True

    def _initialize_provider(self, llm_settings):
        self.logger.info(f"Initializing provider with settings: {llm_settings}")
        provider_type = llm_settings["agent_provider"]

        if provider_type == "vllm_server":
            return VLLMServerProvider(
                llm_settings["url"],
                llm_settings["huggingface"],
                llm_settings["huggingface"],
                self.config.openai_compatible_api_key,
            )
        elif provider_type == "llama_cpp_server":
            return LlamaCppServerProvider(llm_settings["url"])
        elif provider_type == "tgi_server":
            return TGIServerProvider(server_address=llm_settings["url"])
        elif provider_type == "llama_cpp_python":
            llama_model = Llama(
                model_path=f"models/{llm_settings['filename']}",
                flash_attn=True,
                n_threads=40,
                n_gpu_layers=81,
                n_batch=1024,
                n_ctx=llm_settings["max_tokens"],
            )
            return LlamaCppPythonProvider(llama_model)
        #elif provider_type == "groq":
        #    return GroqProvider(
        #        base_url=llm_settings["url"],
        #        model=llm_settings["model"],
        #        huggingface_model=llm_settings["huggingface"],
        #        api_key=llm_settings["api_key"]
        #    )
        elif provider_type == "llama_cpp_python_server":
            return LlamaCppServerProvider(llm_settings["url"], llama_cpp_python_server=True)
        else:
            self.logger.error(f"Unsupported provider: {provider_type}")
            raise ValueError(f"Unsupported provider: {provider_type}")

    def _initialize_agent(self, system_prompt, predefined_messages_formatter_type=MessagesFormatterType.MISTRAL):
        self.logger.info("Initializing LlamaCppAgent.")
        return LlamaCppAgent(
            self.provider,
            debug_output=True,
            system_prompt=system_prompt,
            predefined_messages_formatter_type=predefined_messages_formatter_type,
        )
