import fastapi
from fastapi.responses import JSONResponse
from fastapi import Request, routing
from pydantic import BaseModel
from ..utils.llm import llm_find_entities

router = fastapi.APIRouter()

class MaskRequest(BaseModel):
    text: str

@router.post("/mask", response_class=JSONResponse, include_in_schema=False)
async def mask(request: MaskRequest):
    entities = llm_find_entities(request.text)
    return {"original_text": request.text, "llm_entities": entities}