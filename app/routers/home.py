from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.home_service import HomeService

router = APIRouter(tags=["Home"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
            "title": "Home",
            "active_page": "home",
            "home_data": HomeService.get_homepage_data()
        }
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):

    return templates.TemplateResponse(
        "pages/about.html",
        {
            "request": request,
            "title": "About",
            "active_page": "about"
        }
    )