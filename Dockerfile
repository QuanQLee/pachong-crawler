FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    fi

ENTRYPOINT ["python", "crawler.py"]
