import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Get the absolute path to the directory containing main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the templates directory relative to main.py
# Since main.py is in backend/app/, and frontend/templates is in the project root,
# the relative path is ../../frontend/templates
templates_dir = os.path.abspath(os.path.join(BASE_DIR, "../../frontend/templates"))

# Initialize Jinja2Templates with the correct directory
templates = Jinja2Templates(directory=templates_dir)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


# @app.get("/test")
# def test_route():
#     return {"message": "Test route is working!"}
