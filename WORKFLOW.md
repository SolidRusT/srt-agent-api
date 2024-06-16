# Workflow for Running Tests

## Overview

This document outlines the steps to run tests locally and describes the CI workflow.

## Running Tests Locally

To run the tests locally, follow these steps:

1. Ensure all dependencies are installed:

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # Windows uses the 'Scripts' directory.
    pip install --upgrade pip
    pip install ".[vllm_provider,search_module,wiki_summary_module,wikipedia_query_module]"
    ```

2. Configure a valid `config.yaml`:

3. Run the tests using the provided script:

    ```bash
    python -m app.test_runner
    ```

## CI Workflow

The CI workflow is configured in `.github/workflows/ci.yml` and includes the following steps:

1. **Checkout code**: Checks out the repository.
2. **Set up Python**: Sets up Python 3.11.
3. **Install dependencies**: Installs all required dependencies.
4. **Create config file**: Copies the example configuration file.
5. **Build package**: Builds the Python package.
6. **Run tests**: Executes the test suite.
7. **Clean up build artifacts**: Removes build artifacts to keep the environment clean.

Refer to the [README.md](README.md) for general usage information.
