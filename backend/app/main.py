from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.homepage import router as homepage_router
from backend.app.api.resume import router as resume_router

# Load environment variables
load_dotenv()

# Get the absolute path to the directory containing main.py
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

# Define the templates directory relative to main.py
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "frontend" / "templates"))


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount(
        "/static",
        StaticFiles(directory=str(PROJECT_ROOT / "frontend" / "static")),
        name="static",
    )
    app.include_router(homepage_router)
    app.include_router(resume_router)
    return app


app: FastAPI = create_app()


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(str(PROJECT_ROOT / "frontend" / "static" / "favicon.svg"), media_type="image/svg+xml")


@app.get("/favicon.svg", include_in_schema=False)
async def favicon_svg() -> FileResponse:
    return FileResponse(str(PROJECT_ROOT / "frontend" / "static" / "favicon.svg"), media_type="image/svg+xml")
