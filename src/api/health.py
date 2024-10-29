import fastapi
from fastapi.responses import JSONResponse
from fastapi import Request, routing

router = fastapi.APIRouter()

@router.get("/health", response_class=JSONResponse, include_in_schema=False)
def health(): 
    return {"status": "ok"}