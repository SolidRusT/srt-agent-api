from llama_cpp_agent import AgentChainElement, AgentChain, LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.providers import LlamaCppServerProvider
from srt_core.config import Config
from srt_core.utils.logger import Logger


class ProductComparisonModule:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.dependencies_available = self._check_dependencies()

        if self.dependencies_available:
            self.provider = self._initialize_provider()
            self.agent = self._initialize_agent()
            self.chain = self._initialize_chain()
        else:
            self.logger.info("Product Comparison module dependencies are not installed. Disabling functionality.")

    def _check_dependencies(self):
        required_modules = ["llama_cpp_agent"]
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                self.logger.warning(f"Module {module} is not installed.")
                missing_modules.append(module)
        if missing_modules:
            self.logger.error(f"Missing required modules: {', '.join(missing_modules)}")
            return False
        return True

    def _initialize_provider(self):
        llm_settings = self.config.default_llm_settings
        if llm_settings["agent_provider"] == "llama_cpp_server":
            return LlamaCppServerProvider(llm_settings["url"])
        else:
            self.logger.error(f"Unsupported provider: {llm_settings['agent_provider']}")
            raise ValueError(f"Unsupported provider: {llm_settings['agent_provider']}")

    def _initialize_agent(self):
        return LlamaCppAgent(
            self.provider,
            debug_output=True,
            system_prompt="",
            predefined_messages_formatter_type=MessagesFormatterType.MISTRAL
        )

    def _initialize_chain(self):
        product_comparison = AgentChainElement(
            output_identifier="out_0",
            system_prompt="You are a product comparison expert",
            prompt="Compare the features and specifications of {product1} and {product2} in the {category} category."
        )
        product_recommendation = AgentChainElement(
            output_identifier="out_1",
            system_prompt="You are a product recommendation assistant",
            prompt="Based on the following product comparison, provide a recommendation on which product is better suited for {user_profile}:\n--\n{out_0}"
        )
        return AgentChain(self.agent, [product_comparison, product_recommendation])

    def compare_and_recommend(self, product1, product2, category, user_profile):
        if not self.dependencies_available:
            return "Product Comparison functionality is disabled due to missing dependencies."

        additional_fields = {
            "product1": product1,
            "product2": product2,
            "category": category,
            "user_profile": user_profile
        }
        result = self.chain.run_chain(additional_fields)
        return result


# Example usage
if __name__ == "__main__":
    config = Config()
    logger = Logger()
    product_module = ProductComparisonModule(config, logger)
    result = product_module.compare_and_recommend("iPhone 13", "Samsung Galaxy S22", "Smartphones",
                                                  "a professional photographer")
    print(result)