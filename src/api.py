from fastapi import FastAPI
from pydantic import BaseModel
from src.llm import llm_find_entities

app = FastAPI()

class MaskRequest(BaseModel):
    text: str

@app.get("/")
async def self():
    return {"name": "yo-yo-maskᴙ"}

@app.post("/")
async def mask(request: MaskRequest):
    entities = llm_find_entities(request.text)
    return {"original_text": request.text, "llm_entities": entities}

# curl -X POST "http://localhost:8000" -H "Content-Type: application/json" -d '{"name": "YoYo"}'
