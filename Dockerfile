FROM python:3.13-bookworm

WORKDIR /app

COPY ./requirements.txt .

RUN "./install_dependencies.sh"

COPY . /app/

EXPOSE 8000

CMD ["fastapi", "run", "src/api.py"]