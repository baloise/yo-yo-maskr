from dotenv import load_dotenv
import os
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
HTTPX_CLIENT_VERIFY = os.getenv("HTTPX_CLIENT_VERIFY")
HOST_FLAVOR = os.getenv("HOST_FLAVOR")
