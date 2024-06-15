import unittest
import requests
from unittest.mock import patch, Mock
from app.modules.api_module import APIModule
from srt_core.config import Config
from srt_core.utils.logger import Logger

class TestAPIModule(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.api_module = APIModule(self.config, self.logger)

    @patch('app.modules.api_module.requests.get')
    def test_fetch_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'key': 'value'}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        data = self.api_module.fetch_data('https://example.com/api')
        self.assertEqual(data, {'key': 'value'})

    @patch('app.modules.api_module.requests.get')
    def test_fetch_data_failure(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_get.return_value = mock_response

        data = self.api_module.fetch_data('https://example.com/api')
        self.assertIsNone(data)

    @patch('app.modules.api_module.requests.get')
    def test_fetch_data_list_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{'key': 'value'}, {'key': 'value2'}]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        data_list = self.api_module.fetch_data_list('https://example.com/api')
        self.assertEqual(data_list, [{'key': 'value'}, {'key': 'value2'}])

    @patch('app.modules.api_module.requests.get')
    def test_fetch_data_list_failure(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_get.return_value = mock_response

        data_list = self.api_module.fetch_data_list('https://example.com/api')
        self.assertIsNone(data_list)

if __name__ == '__main__':
    unittest.main()
