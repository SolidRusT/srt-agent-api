# srt-web-chat

## Overview

`srt-web-chat` is a modular application that provides chat functionality using the `llama-cpp-agent` framework and various other features like API fetching.

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
pip install ".[wiki_tool]"
```

## Configuration

Copy `config-example.yaml` to `config.yaml` and customize it according to your needs.

```bash
cp config-example.yaml config.yaml
```

## Usage

Run the application:

```bash
python src/app.py
```

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

## Logging

Logs are stored in the `logs` directory. You can check the logs for detailed information about the application's behavior and any issues encountered.

## Contributing

Feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/SolidRusT/srt-web-chat).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
