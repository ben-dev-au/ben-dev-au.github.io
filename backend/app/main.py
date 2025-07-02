from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import _TemplateResponse


# Local Imports
from . import models, database

# Load environment variables
load_dotenv()

# Get the absolute path to the directory containing main.py
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

# Define the templates directory relative to main.py
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "frontend" / "templates"))


# Dependency to get the database session
def get_db():
    db: Session = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Remove asynccontextmanager and redis usage from lifespan
async def lifespan(app):
    models.Base.metadata.create_all(bind=database.engine)
    yield


# Create the FastAPI app with a lifespan
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise Jinja2Templates with the correct directory
app.mount(
    "/static",
    StaticFiles(directory=str(PROJECT_ROOT / "frontend" / "static")),
    name="static",
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)) -> _TemplateResponse:
    projects: list[models.Project] = db.query(models.Project).all()
    context = {"request": request, "projects": projects}
    return templates.TemplateResponse("homepage/index.html", context)


@app.get("/resume", response_class=HTMLResponse)
async def read_resume(request: Request) -> _TemplateResponse:
    """
    Renders the resume.html template, passing data to it.  Separate route.
    """
    context = {"request": request, "resume_title": "My Resume"}
    return templates.TemplateResponse("resume/resume.html", context)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(str(PROJECT_ROOT / "frontend" / "static" / "favicon.svg"), media_type="image/svg+xml")


@app.get("/favicon.svg", include_in_schema=False)
async def favicon_svg() -> FileResponse:
    return FileResponse(str(PROJECT_ROOT / "frontend" / "static" / "favicon.svg"), media_type="image/svg+xml")
