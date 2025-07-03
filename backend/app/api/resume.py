from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import _TemplateResponse
from pathlib import Path
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR: Path = (Path(__file__).resolve().parents[3] / "frontend" / "templates").absolute()
# print(f"[DEBUG] Jinja2 template directory: {TEMPLATES_DIR}")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


@router.get("/resume", response_class=HTMLResponse)
async def read_resume(request: Request) -> _TemplateResponse:
    context = {"request": request, "resume_title": "My Resume"}
    return templates.TemplateResponse("resume/resume.html", context)
