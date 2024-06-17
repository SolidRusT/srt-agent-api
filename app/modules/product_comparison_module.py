from llama_cpp_agent import AgentChainElement, AgentChain
from app.modules.base_module import BaseModule


class ProductComparisonModule(BaseModule):
    def __init__(self, config, logger):
        required_modules = ["llama_cpp_agent"]
        super().__init__(config, logger, required_modules)

        if self.dependencies_available:
            self.provider = self._initialize_provider()
            self.agent = self._initialize_agent("You are a product comparison expert.")
            self.chain = self._initialize_chain()
        else:
            self.logger.info("Product Comparison module dependencies are not installed. Disabling functionality.")

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
