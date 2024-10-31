import fastapi
from fastapi.responses import JSONResponse
from fastapi import Request, routing
from pydantic import BaseModel
from src.utils.llm import llm_find_entities
from src.utils.replacer import replace_values

router = fastapi.APIRouter()

class MaskRequest(BaseModel):
    text: str

@router.post("/mask", response_class=JSONResponse, include_in_schema=True)
async def mask(request: MaskRequest):
    entities = llm_find_entities(request.text)
    anontext = replace_values(request.text, entities)
    return {"original_text": request.text, "llm_entities": entities, "anonymized_text": anontext}