from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for the input data
class ValueRequest(BaseModel):
    name: str

@app.get("/")
async def generic_greeter():
    return {"message": "Hello, World!"}

@app.post("/")
async def named_greeter(request: ValueRequest):
    return {"name": request.name, "message": f'Hello, {request.name}'}

# curl -X POST "http://localhost:8000" -H "Content-Type: application/json" -d '{"name": "YoYo"}'
