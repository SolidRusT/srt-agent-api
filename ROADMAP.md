# Project Roadmap

This document outlines the future objectives and plans for the `srt-agent-api` project.

## Current Status

The project currently supports the following functionalities:

- Chat module with API and CLI interfaces.
- API endpoints for fetching data, wiki summaries, Wikipedia queries, web searches, and translations.
- Configurable via `config.yaml`.
- CI/CD pipeline set up for automated testing.
- Dockerization with Docker and Docker Compose support.

## Future Objectives

### Leveraging `llama-cpp-agent` Framework

1. **Incorporate More Tools**
   - Explore additional tools provided by the `llama-cpp-agent` and see how they can be integrated.

2. **Refine Existing Modules**
   - Use examples from `llama-cpp-agent` to refine and enhance current modules, improving their functionality and performance.

3. **New Functionality**
   - Explore new functionalities inspired by the `llama-cpp-agent` repository that can be added to our current setup.

### New Module Ideas

1. **Translation Module**
   - Implemented. Continue refining and expanding language support using the `llama-cpp-agent` framework.

2. **Sentiment Analysis Module**
   - Create a tool to analyze the sentiment of text inputs.

3. **Summarization Module**
   - Develop a module for text summarization, different from the wiki summary.

4. **Entity Recognition Module**
   - Implement a tool that identifies and extracts entities from text.

### Improve Documentation and Developer Experience

1. **API Documentation**
   - Create detailed API documentation using tools like Swagger.

2. **Example Use Cases**
   - Provide more example use cases and code snippets for developers.

3. **Tutorials and Guides**
   - Develop tutorials and guides to help new users get started with the project.

### Enhance Testing and CI/CD

1. **Increase Test Coverage**
   - Write more unit and integration tests to cover all functionalities.

2. **Automate Deployment**
   - Set up CI/CD pipelines to automate deployment to a cloud service.

3. **Mocking External Services**
   - Ensure tests don't rely on external services by mocking them.

### Performance, Concurrency, and Accuracy

1. **Distributed Architecture**
   - Enable modules to run on different machines or ports for better control over dependencies and scaling.

2. **Prometheus Integration**
   - Utilize `prometheus-node-exporter` for additional monitoring of the Ubuntu Server 24.04 machines.

## Prioritization and Phases

### Phase 1: Immediate Goals

- **Leverage `llama-cpp-agent` Examples**
  - Incorporate more tools.
  - Refine existing modules.
- **Improve Documentation and Developer Experience**
  - Create detailed API documentation.

### Phase 2: Near-term Goals

- **New Module Ideas**
  - Sentiment Analysis Module.
  - Summarization Module.
- **Enhance Testing and CI/CD**
  - Increase test coverage.

### Phase 3: Long-term Goals

- **Distributed Architecture**
  - Enable distributed architecture for better performance and scalability.
- **New Module Ideas**
  - Entity Recognition Module.
- **Prometheus Integration**
  - Integrate Prometheus for enhanced monitoring and performance tracking.

## Conclusion

This roadmap will be regularly updated to reflect the progress and changes in priorities. Contributions and suggestions are welcome!

## References

- [llama-cpp-agent Examples Repository](https://github.com/Maximilian-Winter/llama-cpp-agent/tree/master/examples)
