FROM python:3.13-bookworm

LABEL maintainer="culmat, trichie, robbizbal" \
      description="Yo-Yo-Maskr application Docker image" \
      version="0.1.0"

WORKDIR /app

COPY . /app/

RUN "./install_dependencies.sh"

EXPOSE 8000

CMD ["fastapi", "run", "src/api.py"]