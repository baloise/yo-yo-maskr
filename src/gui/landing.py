import fastapi
from fastapi.responses import HTMLResponse
from fastapi import Request, routing
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/templates")

router = fastapi.APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def landing(request: Request): 
    return templates.TemplateResponse(
        request=request, name="form.html", context={"id": id}
    )
