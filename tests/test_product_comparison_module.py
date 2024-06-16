import unittest
from unittest.mock import patch, Mock
from app.modules.product_comparison_module import ProductComparisonModule
from srt_core.config import Config
from srt_core.utils.logger import Logger

class TestProductComparisonModule(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.module = ProductComparisonModule(self.config, self.logger)

    @patch('app.modules.product_comparison_module.LlamaCppAgent')
    def test_compare_and_recommend(self, MockAgent):
        mock_agent = MockAgent.return_value
        mock_agent.run_chain.return_value = "Recommended Product: iPhone 13"

        result = self.module.compare_and_recommend("iPhone 13", "Samsung Galaxy S22", "Smartphones", "a professional photographer")
        self.assertEqual(result, "Recommended Product: iPhone 13")

if __name__ == '__main__':
    unittest.main()
