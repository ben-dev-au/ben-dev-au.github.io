from pathlib import Path
import os
from pydantic import SecretStr

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

# import ssl
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware


# Local Imports
from . import models, database, schemas

# Load environment variables
load_dotenv()

# Get the absolute path to the directory containing main.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the templates directory relative to main.py
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "frontend" / "templates"))

# Email configuration
email_conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME") or "",
    MAIL_PASSWORD=SecretStr(os.getenv("MAIL_PASSWORD") or ""),
    MAIL_FROM=os.getenv("MAIL_FROM") or "",
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER") or "",
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


@asynccontextmanager
async def lifespan(app):
    models.Base.metadata.create_all(bind=database.engine)

    # Only initialise Redis if we're in production or if Redis is available locally
    redis_url = os.getenv("REDIS_URL")
    if redis_url or os.getenv("ENVIRONMENT") == "production":
        try:
            # Connect to Redis
            redis_connection = await redis.from_url(
                redis_url or "redis://localhost:6379",
                encoding="utf-8",
                decode_responses=True,
                ssl_cert_reqs=None,  # Disable SSL cert verification
            )

            # Initialise FastAPILimiter
            await FastAPILimiter.init(redis_connection)
        except Exception as e:
            if os.getenv("ENVIRONMENT") == "production":
                # In production, Redis is required
                raise e
            # In development, just log the error and continue without Redis
            print(f"Redis connection failed: {e}. Continuing without rate limiting.")

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


class CsrfSettings(BaseModel):
    secret_key: str = os.getenv("SECRET_KEY") or ""


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return HTMLResponse("CSRF token missing or invalid", status_code=400)


@app.get("/contact", response_class=HTMLResponse)
async def get_contact(request: Request, csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.generate_csrf_tokens()
    context = {"request": request, "csrf_token": csrf_token}
    return templates.TemplateResponse("homepage/index.html", context)


# Route for getting the contact form page.
@app.post("/contact", response_class=HTMLResponse)
async def handle_contact(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
    csrf_token: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
    rate_limiter: RateLimiter = Depends(RateLimiter(times=5, seconds=60)),
):
    await csrf_protect.validate_csrf(request, csrf_token)

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
        recipient_email = os.getenv("RECIPIENT_EMAIL")
        if recipient_email:
            email_message = MessageSchema(
                subject=f"New Contact Form Submission from {name}",
                recipients=[recipient_email],
                body=f"""Name: {name}
Email: {email}
Message: {message}""",
                subtype=MessageType.plain,
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


@app.get("/resume", response_class=HTMLResponse)
async def read_resume(request: Request):
    """
    Renders the resume.html template, passing data to it.  Separate route.
    """
    context = {"request": request, "resume_title": "My Resume"}
    return templates.TemplateResponse("resume/resume.html", context)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(str(PROJECT_ROOT / "frontend" / "static" / "favicon.svg"), media_type="image/svg+xml")


@app.get("/favicon.svg", include_in_schema=False)
async def favicon_svg():
    return FileResponse(str(PROJECT_ROOT / "frontend" / "static" / "favicon.svg"), media_type="image/svg+xml")
