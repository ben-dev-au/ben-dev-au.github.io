from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Get the absolute path to the directory containing main.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the templates directory relative to main.py
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "frontend" / "templates"))


# Initialize Jinja2Templates with the correct directory
app.mount(
    "/static",
    StaticFiles(directory=str(PROJECT_ROOT / "frontend" / "static")),
    name="static",
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()

    context = {"request": request, "projects": projects}
    return templates.TemplateResponse("homepage/index.html", context)


@app.get("/index2", response_class=HTMLResponse)
async def index2(request: Request, db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()

    context = {"request": request, "projects": projects}
    return templates.TemplateResponse("homepage/index2.html", context)


@app.get("/resume", response_class=HTMLResponse)  # for testing purposes
async def read_resume(request: Request):
    """
    Renders the resume.html template, passing data to it.  Separate route.
    """
    context = {"request": request, "resume_title": "My Resume"}
    return templates.TemplateResponse("resume/resume.html", context)
