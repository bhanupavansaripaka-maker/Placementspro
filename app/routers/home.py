from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.data.home import HOME_STATISTICS

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
            "active_page": "home",
            "statistics": HOME_STATISTICS
        }
    )