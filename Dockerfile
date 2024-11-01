FROM --platform=linux/amd64 python:3.12.7-slim-bookworm

# set metadata
LABEL maintainer="culmat, trichie, robbizbal" \
      org.opencontainers.image.description="Yo-Yo-Maskr application Docker image" \
      version="0.1.0"

# expose port
EXPOSE 8000

# set poetry environment variables
ARG POETRY_FLAGS="--only main"
ARG LOAD_NER_MODELS="False"

# set default environment variables
ENV OLLAMA_BASE_URL=http://localhost:11434 \
    OLLAMA_MODEL=llama3.2:latest \
    DEBIAN_FRONTEND=noninteractive \
    HTTPX_CLIENT_VERIFY=

# add app src
COPY . /app/

# set workdir
WORKDIR /app

# set script permissions
RUN chmod +x entrypoint.sh docker_setup.sh

RUN apt -y update \
    && apt install -y make \
    && apt clean autoclean \
    && rm -rf /var/lib/apt/lists/*

# create user
#RUN useradd -ms /bin/bash anon && chown -R anon: /app
RUN useradd -ms /bin/bash -G 0 anon

# set permissions - for OpenShift
RUN chgrp -R 0 /app && chown -R anon:0 /app && chmod -R g+rwX /app

# switch to user
USER anon

# set workdir
WORKDIR /app

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install pipx \
    && python3 -m pipx ensurepath \
    && python3 -m pipx completions

# run app setup script
RUN "./docker_setup.sh"

# run app
ENTRYPOINT ["/app/entrypoint.sh"]