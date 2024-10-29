import fastapi
from fastapi.responses import HTMLResponse
from fastapi import Request, routing

router = fastapi.APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def landing(): 
    return "<h1>hola mundo</h1>"