# Use an official Python runtime as a base image
FROM python:3.13-bookworm

WORKDIR /app

COPY . /app/

RUN "./install_dependencies.sh"

EXPOSE 8000

CMD ["fastapi", "run", "yoyomaskr/api.py"]