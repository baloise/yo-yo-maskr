FROM python:3.13-bookworm

WORKDIR /app

COPY . /app/

RUN "./install_dependencies.sh"

EXPOSE 8000

CMD ["fastapi", "run", "src/api.py"]