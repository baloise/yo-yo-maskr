import fastapi
from fastapi.responses import HTMLResponse
from fastapi import Request, routing
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/templates/html")

router = fastapi.APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def landing(request: Request): 
    return templates.TemplateResponse(
        request=request, name="landing.html", context={"id": id}
    )