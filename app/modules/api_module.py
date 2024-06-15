import requests
from srt_core.config import Config
from srt_core.utils.logger import Logger

class APIModule:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch data from {url}: {e}")
            return None

    def fetch_data_list(self, url):
        data = self.fetch_data(url)
        if data:
            return [item for item in data]
        else:
            return []

# Example usage
if __name__ == "__main__":
    config = Config()
    logger = Logger()
    api_module = APIModule(config, logger)
    data = api_module.fetch_data("https://jsonplaceholder.typicode.com/posts/1")
    print(f"Fetched Data: {data}")
    data_list = api_module.fetch_data_list("https://jsonplaceholder.typicode.com/posts")
    print(f"Fetched Data List: {data_list}")
