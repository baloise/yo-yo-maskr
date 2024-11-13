import fastapi
from fastapi.responses import JSONResponse
from fastapi import Request
from enum import Enum
from pydantic import BaseModel
from src.utils.ano_llm import find_entities as llm_find_entities
from src.utils.ano_spacy import Anon_Spacy
from src.utils.ano_regex import find_entities as reg_find_entities
from src.utils.env import *

router = fastapi.APIRouter()

class BackendType(Enum):
    LLM = "LLM"
    NER = "NER"
    REG = "REG"

class MaskRequest(BaseModel):
    text: str
    backendType: BackendType
    llmURL: str
    llmModel: str

ano = Anon_Spacy()

def check_parameter(param):
   if not param:  # This checks if param is empty (None, '', [], etc.)
        print(f"The parameter is empty. Setting to default value from ENV if existing.")
        return 0
   else:
        print(f"The parameter is not empty: {param}")
        return 1

@router.post("/mask", response_class=JSONResponse, include_in_schema=True)
async def mask(request: MaskRequest):
    
    match request.backendType:
        case BackendType.LLM:
            if check_parameter(request.llmURL) == 0:
                request.llmURL = OLLAMA_BASE_URL
            
            if check_parameter(request.llmModel) == 0:
                request.llmModel = OLLAMA_MODEL

            llm_entities = llm_find_entities(text=request.text, base_url=request.llmURL, model=request.llmModel)
            return {"original_text": request.text.strip().replace('"', ''), "entities": llm_entities['replace_dict'], "anonymized_text": llm_entities['text'].strip().replace('"', '')}
        case BackendType.NER:
            spacy_entities = ano.find_entities(request.text)
            return {"original_text": request.text.strip().replace('"', ''), "entities": spacy_entities['replace_dict'], "anonymized_text": spacy_entities['text'].strip().replace('"', '')}
        case BackendType.REG:
            regex_entities = reg_find_entities(request.text)
            return {"original_text": request.text.strip().replace('"', ''), "entities": regex_entities['replace_dict'], "anonymized_text": regex_entities['text'].strip().replace('"', '')}
        case _:
            return {"original_text": "Invalid backend type"}