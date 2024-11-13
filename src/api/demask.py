import fastapi
from fastapi.responses import JSONResponse
from fastapi import Request
from pydantic import BaseModel
from src.utils.replacer import revert_replacements

router = fastapi.APIRouter()

class MaskRequest(BaseModel):
    text: str
    entities: dict

@router.post("/demask", response_class=JSONResponse, include_in_schema=True)
async def mask(request: MaskRequest):
    deanontext = revert_replacements(request.text, request.entities)
    return {"deanonymized_text": deanontext.strip().replace('"', '')}