from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


@router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={},
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={},
    )


@router.get("/planner/{planner}", response_class=HTMLResponse)
def planner(request: Request, planner: str):
    allowed = {
        "home",
        "party",
        "jewelry",
    }

    if planner not in allowed:
        planner = "home"

    return templates.TemplateResponse(
        request=request,
        name=f"{planner}_planner.html",
        context={
            "planner": planner,
        },
    )


@router.get("/history", response_class=HTMLResponse)
def history(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={},
    )


@router.get(
    "/recommendation/{recommendation_id}",
    response_class=HTMLResponse,
)
def recommendation(request: Request, recommendation_id: int):
    return templates.TemplateResponse(
        request=request,
        name="recommendation.html",
        context={
            "recommendation_id": recommendation_id,
        },
    )


@router.get("/testimonials", response_class=HTMLResponse)
def testimonials(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="testimonials.html",
        context={},
    )