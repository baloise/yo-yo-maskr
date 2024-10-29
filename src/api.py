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

@app.get("/health")
async def health(): 
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 


## notes
# curl -X POST "http://localhost:8000" -H "Content-Type: application/json" -d '{"name": "YoYo"}'