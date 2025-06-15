# Pachong Crawler

Pachong Crawler is an experimental web crawling project. It aims to demonstrate basic crawling
concepts in a simple, modular way while respecting website policies and minimizing impact on
resources.

## Purpose

The repository showcases a minimal setup for building crawlers that respect `robots.txt` rules
and implement polite crawling practices. It is not intended for large scale or commercial use.

## Features

- **Robots.txt compliance** using libraries that parse and obey site policies.
- **Rate limiting** with configurable delays between requests.
- Optional **proxy support** for requests.
- Simple **modular structure** that can be extended for specific targets.

## Basic Usage Examples

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main crawler script
python crawler.py --url https://example.com
```

## Docker Usage

```bash
# Build the image
docker build -t pachong-crawler .

# Run the container with a target URL
docker run pachong-crawler --url https://example.com
```

## Contribution Guidelines

1. Fork the repository and create a feature branch.
2. Follow best practices for robots.txt compliance and respectful crawling.
3. Submit a pull request describing your changes.

## Roadmap

- Add tests for robots.txt parsing.
- Provide a configuration file for rate limits and proxies.
- Implement more robust error handling.

