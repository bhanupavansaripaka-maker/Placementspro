from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.home_service import get_home_page_data

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):

    data = get_home_page_data()

    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
            "active_page": "home",
            **data
        }
    )