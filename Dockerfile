FROM alpine:latest

# set metadata
LABEL maintainer="culmat, trichie, robbizbal" \
      org.opencontainers.image.description="Yo-Yo-Maskr application Docker image" \
      version="0.1.0"

# set poetry environment variables
ARG POETRY_FLAGS="--without dev"

# set default environment variables
ENV OLLAMA_BASE_URL=http://localhost:11434 \
    OLLAMA_MODEL=llama3.2:latest \
    HTTPX_CLIENT_VERIFY=

# install Python and dependencies
RUN apk add --no-cache --update \
    python3 \
    py3-pip \
    gcc \
    python3-dev \
    make \
    bash \
    && rm -rf ~/.cache/* /usr/local/share/man /tmp/*

RUN python3 -m pip install pipx --break-system-packages \
    && python3 -m pipx ensurepath \
    && python3 -m pipx completions 

# add app src
COPY . /app/

# set workdir
WORKDIR /app

# set script permissions
RUN chmod +x entrypoint.sh setup.sh

# create user
RUN adduser -Ds /bin/bash anon && chown -R anon: /app

# switch to user
USER anon

# run app setup script
RUN "./setup.sh"

# expose port
EXPOSE 8000

# run app
ENTRYPOINT ["/app/entrypoint.sh"]