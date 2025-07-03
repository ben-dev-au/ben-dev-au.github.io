from typing import List
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.templating import _TemplateResponse
from backend.app.models.project import Project
from backend.app.services.db import get_db
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR: Path = (Path(__file__).resolve().parents[3] / "frontend" / "templates").absolute()
# print(f"[DEBUG] Jinja2 template directory: {TEMPLATES_DIR}")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)) -> _TemplateResponse:
    projects: List[Project] = db.query(Project).all()
    print(f"[DEBUG] Projects from DB: {projects}")
    context = {"request": request, "projects": projects}
    return templates.TemplateResponse("homepage/index.html", context)
