from pathlib import Path
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

# import ssl

# Local Imports
from . import models, database, schemas


# from fastapi.responses import HTMLResponse, RedirectResponse

# models.Base.metadata.create_all(bind=database.engine)

# Load environment variables
load_dotenv()

# app = FastAPI()

# Get the absolute path to the directory containing main.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the templates directory relative to main.py
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "frontend" / "templates"))

# Email configuration
email_conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
)


# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Lifespan function to create tables at startup
@asynccontextmanager
async def lifespan(app):
    # Create database tables if needed.
    models.Base.metadata.create_all(bind=database.engine)

    # Use Heroku's provided Redis URL (or default to localhost).
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Create the connection without extra SSL parameters.
    redis_connection = await redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

    # Initialise FastAPILimiter.
    await FastAPILimiter.init(redis_connection)

    yield


# Create the FastAPI app with a lifespan
app = FastAPI(lifespan=lifespan)

# Initialise Jinja2Templates with the correct directory
app.mount(
    "/static",
    StaticFiles(directory=str(PROJECT_ROOT / "frontend" / "static")),
    name="static",
)


class CsrfSettings(BaseModel):
    secret_key: str = os.getenv("SECRET_KEY")


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return HTMLResponse("CSRF token missing or invalid", status_code=400)
    # # Removed deprecated startup event; logic moved to lifespan handler.
    # redis_connection = await redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    # await FastAPILimiter.init(redis_connection)


@app.get("/contact", response_class=HTMLResponse)
async def get_contact(request: Request, csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.generate_csrf()
    context = {"request": request, "csrf_token": csrf_token}
    return templates.TemplateResponse("homepage/index.html", context)


# Route for getting the contact form page.
@app.post("/contact", dependencies=[Depends(RateLimiter(times=5, seconds=60))], response_class=HTMLResponse)
async def handle_contact(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
    csrf_token: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
    # prettier-ignore
):

    csrf_protect.validate_csrf(csrf_token)

    # Validate form data using Pydantic
    try:
        contact_data = schemas.ContactForm(
            name=name,
            email=email,
            message=message,
            # prettier-ignore
        )
    except Exception:
        # Handle validation errors
        context = {"request": request, "error": "Invalid form data. Please check your inputs."}
        return templates.TemplateResponse("homepage/index.html", context)

    # Process the contact message and save to database.
    new_message = models.ContactMessage(
        name=contact_data.name,
        email=contact_data.email,
        message=contact_data.message,
        # prettier-ignore
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Send an email notification
    try:
        email_message = MessageSchema(
            subject=f"New Contact Form Submission from {name}",
            recipients=[os.getenv("RECIPIENT_EMAIL")],
            body=f"""Name: {name}
Email: {email}
Message: {message}""",
            subtype="plain",
        )
        fm = FastMail(email_conf)
        await fm.send_message(email_message)
    except Exception as e:
        # Log the error, but do not expose internal errors to the user
        print(f"Error sending email: {e}")

    # Redirect to render a success message.
    context = {"request": request, "success": "Your message has been sent successfully!"}
    return templates.TemplateResponse("homepage/index.html", context)


# Homepage Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()

    context = {"request": request, "projects": projects}
    return templates.TemplateResponse("homepage/index.html", context)


# @app.get("/index2", response_class=HTMLResponse)
# async def index2(request: Request, db: Session = Depends(get_db)):
#     projects = db.query(models.Project).all()

#     context = {"request": request, "projects": projects}
#     return templates.TemplateResponse("homepage/index2.html", context)


@app.get("/resume", response_class=HTMLResponse)
async def read_resume(request: Request):
    """
    Renders the resume.html template, passing data to it.  Separate route.
    """
    context = {"request": request, "resume_title": "My Resume"}
    return templates.TemplateResponse("resume/resume.html", context)
