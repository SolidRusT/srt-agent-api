# Docker Setup

This document provides instructions for building and running the `srt-agent-api` application using Docker.

## Prerequisites

- Docker installed on your machine.
- Docker Compose installed.

## Building the Docker Image

To build the Docker image, run the following command from the root of the repository:

```bash
docker build -t srt-agent-api .
```

## Running the Docker Container

To run the Docker container, use the following command:

```bash
docker run -d -p 8000:8000 -e PERSONA='Default' -e PORT=8000 -e SERVER_NAME='0.0.0.0' --name srt-agent-api srt-agent-api
```

## Using Docker Compose

A `docker-compose.yml` file is provided for easier management of multiple services. To use Docker Compose, run:

```bash
docker-compose up -d
```

### Example `docker-compose.yml`

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: srt-agent-api
    ports:
      - "8000:8000"
    environment:
      - PERSONA=Default
      - PORT=8000
      - SERVER_NAME=0.0.0.0

  search_module:
    build: .
    container_name: srt-agent-search
    ports:
      - "8001:8001"
    environment:
      - PERSONA=Search
      - PORT=8001
      - SERVER_NAME=0.0.0.0

  wiki_summary_module:
    build: .
    container_name: srt-agent-wiki-summary
    ports:
      - "8002:8002"
    environment:
      - PERSONA=WikiSummary
      - PORT=8002
      - SERVER_NAME=0.0.0.0

  wikipedia_query_module:
    build: .
    container_name: srt-agent-wikipedia-query
    ports:
      - "8003:8003"
    environment:
      - PERSONA=WikipediaQuery
      - PORT=8003
      - SERVER_NAME=0.0.0.0
```

## Accessing the API

Once the containers are running, you can access the API endpoints as described in the [README](README.md) file.

### Health Check

To check if the API service is running, use the health check endpoint:

```bash
curl -X GET "http://127.0.0.1:8000/"
```

## Stopping the Containers

To stop the containers, use the following command:

```bash
docker-compose down
```

## Logging

Logs can be accessed using the Docker logs command:

```bash
docker logs srt-agent-api
```

For Docker Compose, you can specify the service name:

```bash
docker-compose logs api
```

## Contributing

Feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/SolidRusT/srt-agent-api).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
