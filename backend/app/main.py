from pathlib import Path
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database, schemas

from contextlib import asynccontextmanager

# from fastapi.responses import HTMLResponse, RedirectResponse

# models.Base.metadata.create_all(bind=database.engine)

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


# Startup event to create tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    yield


app.router.lifespan_context = lifespan


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


@app.post("/contact", response_class=HTMLResponse)
async def handle_contact(
    request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...), db: Session = Depends(get_db)
):
    # Validate form data using Pydantic
    try:
        contact_data = schemas.ContactForm(name=name, email=email, message=message)
    except Exception:
        # Handle validation errors
        context = {"request": request, "error": "Invalid form data. Please check your inputs."}
        return templates.TemplateResponse("contact.html", context)

    # Process the data (e.g., save to database)
    new_message = models.ContactMessage(name=contact_data.name, email=contact_data.email, message=contact_data.message)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Redirect to a thank you page or render a success message
    context = {"request": request, "success": "Your message has been sent successfully!"}
    return templates.TemplateResponse("contact.html", context)


@app.get("/contact", response_class=HTMLResponse)
async def get_contact(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("contact.html", context)
