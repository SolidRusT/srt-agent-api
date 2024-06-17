# srt-agent-api

![GitHub Release](https://img.shields.io/github/v/release/SolidRusT/srt-agent-api) ![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FSolidRusT%2Fsrt-agent-api%2Fmain%2Fpyproject.toml) ![GitHub License](https://img.shields.io/github/license/SolidRusT/srt-agent-api)

## Overview

`srt-agent-api` is a modular application that provides chat functionality using the `llama-cpp-agent` framework and various other features like API fetching and Wikipedia summaries.

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install .
```

To include optional dependencies for the `vllm_provider`:

```bash
pip install ".[vllm_provider]"
```

To include optional dependencies for the `search_module`:

```bash
pip install ".[search_tool]"
```

To include optional dependencies for the `wiki_summary_module`:

```bash
pip install ".[wiki_summary_module]"
```

To include optional dependencies for the `wikipedia_query_module`:

```bash
pip install ".[wikipedia_query_module]"
```

## Configuration

Copy `config-example.yaml` to `config.yaml` and customize it according to your needs.

```bash
cp config-example.yaml config.yaml
```

## Usage

To start the API service:

```bash
export PERSONA='Default'       # Persona for the 'chat_module'.
export PORT=8000               # TCP port for the API service
export SERVER_NAME='127.0.0.1' # IP to use, or for all IPs: '0.0.0.0'

python -m app.api_service
```

### Running the Application

To run the CLI client application:

```bash
python -m app.cli_interface
```

### API Documentation

Once the API service is running, you can access the interactive API documentation at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Chat Module

The chat module allows you to interact with the assistant:

```plaintext
> Hi, my name is Jeff.
Agent: Hello, Jeff! How can I assist you today?
```

### API Module

You can fetch data from an API using the `fetch:` command:

```plaintext
> fetch: https://jsonplaceholder.typicode.com/posts/1
Fetched Data: {data}

> fetch_list: https://jsonplaceholder.typicode.com/posts
Fetched Data List: [{data1}, {data2}, ...]
```

### Search Module

If the `search_module` dependencies are installed, you can perform searches using the `search:` command:

```plaintext
> search: how to mow the lawn
Search Results: {results}
```

### Wiki Summary Module

If the `wiki_summary_module` dependencies are installed, you can summarize Wikipedia content using the `wiki:` command:

```plaintext
> wiki: Synthetic diamond
Summary: {summary}
```

### Wikipedia Query Module

If the `wikipedia_query_module` dependencies are installed, you can query Wikipedia content using the `wikipedia_query:` command:

```plaintext
> wikipedia_query: Synthetic_diamond, What is a BARS apparatus?
Summary: {summary}
```

### Product Comparison Module

If the `product_comparison_module` dependencies are installed, you can compare products and get recommendations using the `compare:` command:

```plaintext
> compare: iPhone 13, Samsung Galaxy S22, Smartphones, a professional photographer
Product Comparison Result: {result}
```

### Agentic Reflection Module

If the `agentic_reflection_module` dependencies are installed, you can get reflective responses using the `reflect:` command:

```plaintext
> reflect: Write a summary about the independence war of America against England.
Reflective Response: {response}
```

## Dockerization

You can build and run the application using Docker. For detailed instructions, see [DOCKER.md](DOCKER.md).

## API Endpoints

### Health Check

To check if the API service is running, use the health check endpoint:

```bash
curl -X GET "http://127.0.0.1:8000/"
```

### Fetch Data

To fetch data from a URL, use the fetch endpoint:

```bash
curl -X GET "http://127.0.0.1:8000/fetch?url=https://jsonplaceholder.typicode.com/posts/1"
```

### Fetch Data List

To fetch a list of data from a URL, use the fetch list endpoint:

```bash
curl -X GET "http://127.0.0.1:8000/fetch-list?url=https://jsonplaceholder.typicode.com/posts"
```

### Web Search

To get a summary of a Web Search, use the web search endpoint:

```bash
curl -X GET "http://127.0.0.1:8000/search?query=how%20to%20search%20the%20web"
```

### Wiki Summary

To get a summary of a Wikipedia page, use the wiki summary endpoint:

```bash
curl -X GET "http://127.0.0.1:8000/wiki-summary/Python_(programming_language)"
```

### Wikipedia Query

To query a Wikipedia page, use the wikipedia query endpoint:

```bash
curl -X GET "http://127.0.0.1:8000/wikipedia-query?page_url=Synthetic_diamond&query=What%20is%20a%20BARS%20apparatus%3F"
```

### API Endpoint for Product Comparison

To compare products and get a recommendation, use the product comparison endpoint:

```bash
curl -X GET "http://127.0.0.1:8000/product-comparison?product1=iPhone%2013&product2=Samsung%20Galaxy%20S22&category=Smartphones&user_profile=a%20professional%20photographer"
```

### Get Reflective Response

To get a reflective response, use the following endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/reflective-response" -d "input_message=Write a summary about the independence war of America against England."
```

## Logging

Logs are stored in the `logs` directory. You can check the logs for detailed information about the application's behavior and any issues encountered.

## Contributing

Feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/SolidRusT/srt-agent-api).

For detailed information on running tests and the CI workflow, see the [Workflow Documentation](WORKFLOW.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.