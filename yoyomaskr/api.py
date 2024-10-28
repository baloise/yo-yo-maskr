from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MaskRequest(BaseModel):
    text: str

@app.get("/")
async def self():
    return {"name": "yo-yo-maskᴙ"}

@app.post("/")
async def mask(request: MaskRequest):
    return {"masked_text": request.text, "analysis": []}

# curl -X POST "http://localhost:8000" -H "Content-Type: application/json" -d '{"name": "YoYo"}'
