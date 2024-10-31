FROM python:3.12-bookworm

# set metadata
LABEL maintainer="culmat, trichie, robbizbal" \
      org.opencontainers.image.description="Yo-Yo-Maskr application Docker image" \
      version="0.1.0"

# set poetry environment variables
ARG POETRY_FLAGS="--only main"

# set default environment variables
ENV OLLAMA_BASE_URL=http://localhost:11434 \
    OLLAMA_MODEL=llama3.2:latest \
    HTTPX_CLIENT_VERIFY=

# add app src
COPY . /app/

# set workdir
WORKDIR /app

# set script permissions
RUN chmod +x entrypoint.sh setup.sh

# create user
#RUN useradd -ms /bin/bash anon && chown -R anon: /app
RUN useradd -ms /bin/bash -G 0 anon

# set permissions - for OpenShift
RUN chgrp -R 0 /app && chmod -R g+rwX /app

# switch to user
USER anon

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install pipx \
    && python3 -m pipx ensurepath \
    && python3 -m pipx completions

# run app setup script
RUN "./setup.sh"

# expose port
EXPOSE 8000

# run app
ENTRYPOINT ["/app/entrypoint.sh"]