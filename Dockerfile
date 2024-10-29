FROM python:3.13-bookworm

LABEL maintainer="culmat, trichie, robbizbal" \
      description="Yo-Yo-Maskr application Docker image" \
      version="0.1.0"

ENV OLLAMA_BASE_URL=http://localhost:11434 \
    OLLAMA_MODEL=llama3.2:latest \
    HTTPX_CLIENT_VERIFY=

COPY . /app/

WORKDIR /app

RUN "./setup.sh"

EXPOSE 8000

CMD ["make", "run"]