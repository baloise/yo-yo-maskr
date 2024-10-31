import fastapi
from fastapi.responses import JSONResponse
from fastapi import Request
from enum import Enum
from pydantic import BaseModel
from src.utils.ano_llm import find_entities as llm_find_entities
from src.utils.replacer import replace_values
from src.utils.ano_spacy import Anon_Spacy
from src.utils.ano_regex import find_entities as reg_find_entities

router = fastapi.APIRouter()

class BackendType(Enum):
    LLM = "LLM"
    NER = "NER"
    REG = "REG"

class MaskRequest(BaseModel):
    text: str
    backendType: BackendType

ano = Anon_Spacy()

@router.post("/mask", response_class=JSONResponse, include_in_schema=True)
async def mask(request: MaskRequest):
    
    match request.backendType:
        case BackendType.LLM:
            llm_entities = llm_find_entities(request.text)
            anontext = replace_values(request.text, llm_entities)
            return {"original_text": request.text, "entities": llm_entities, "anonymized_text": anontext}
        case BackendType.NER:
            spacy_entities = ano.find_entities(request.text)
            #anontext = replace_values(request.text, spacy_entities.replace_dict)
            anontext="blabla"
            return {"original_text": request.text, "entities": spacy_entities, "anonymized_text": anontext}
        case BackendType.REG:
            regex_entities = reg_find_entities(request.text)
            #anontext = replace_values(request.text, entities)
            anontext="blabla"
            return {"original_text": request.text, "entities": regex_entities, "anonymized_text": anontext}
        case _:
            return {"original_text": "Invalid backend type"}