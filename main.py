from fastapi import FastAPI
from pydantic import BaseModel
from yoyomaskr import llm_find_entities

app = FastAPI()

# Define a Pydantic model for the input data
class ValueRequest(BaseModel):
    text: str

@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}

@app.post("/")
async def llm_entities(request: ValueRequest):
    entities = llm_find_entities(request.text)
    return {"original_text": request.text, "llm_entities": entities}

# curl -X POST "http://localhost:8000" -H "Content-Type: application/json" -d '{"text": "text"}'
