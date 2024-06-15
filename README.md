# srt-web-chat

srt-web-chat is a modular web chat application that integrates the `srt-core` configuration system and the `llama-cpp-agent` framework. It provides a robust foundation for building LLM-based AI agents with flexible configurations and logging.

## Features

- Modular architecture for easy extension and integration.
- Configurable via a YAML file.
- Integrates with `srt-core` for configuration and logging.
- Uses `llama-cpp-agent` for LLM interactions.
- Supports multiple LLM providers.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SolidRusT/srt-web-chat.git
   cd srt-web-chat
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the base dependencies and the project:

   ```bash
   pip install .
   ```

4. Install optional dependencies as needed:

   For vLLM Provider:

   ```bash
   pip install ".[vllm_provider]"
   ```

   For Search Tool:

   ```bash
   pip install ".[search_tool]"
   ```

## Configuration

1. Copy the example configuration file to create your own configuration:

   ```bash
   cp config-example.yaml config.yaml
   ```

2. Customize the `config.yaml` file with your own settings.

## Usage

Run the main application:

```bash
python src/app.py
```

## Building the Project

To build the project, ensure you have the build tool installed:

```bash
pip install build
```

Then, build the project:

```bash
python -m build
```

This will generate the distribution packages in the `dist` directory.

## Running Tests

To run the tests, you can use `unittest` or `pytest`. For example, with `pytest`:

```bash
pip install pytest
pytest
```

## Project Structure

```plaintext
srt-web-chat/
│
├── LICENSE
├── README.md
├── config.yaml
├── pyproject.toml
├── src/
│   ├── app.py
│   ├── chat_module.py
│   ├── llm_provider.py
│   ├── main.py
│   ├── search_module.py
└── tests/
    ├── test_chat_module.py
    ├── test_llm_provider.py
    ├── test_main.py
    └── test_search_module.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For more information, please contact SolidRusT Networks at [info@solidrust.net](mailto:info@solidrust.net).
