# Makefile for portfolio website development

# ────────────────────────
# 1. VARIABLES (override on CLI)
# ────────────────────────
APP_MODULE   := backend.app.main:app
HOST         ?= 127.0.0.1
PORT         ?= 8000

# ────────────────────────
# 2. DEFAULT GOAL
# ────────────────────────
.DEFAULT_GOAL := help

# ────────────────────────
# 3. PHONY TARGETS
# ────────────────────────
.PHONY: help install run lint fmt test clean

# ────────────────────────
# 4. TARGETS
# ────────────────────────

help:
	@echo "Usage: make [target] [VARIABLE=value]"
	@echo ""
	@echo "Targets:"
	@echo "  install    Install dependencies via Poetry"
	@echo "  run        Launch Uvicorn server"
	@echo "  lint       Run flake8 for linting"
	@echo "  fmt        Run black for code formatting"
	@echo "  test       Run pytest"
	@echo "  clean      Remove caches and build artifacts"
	@echo ""
	@echo "You can override HOST and PORT:"
	@echo "  make run HOST=0.0.0.0 PORT=9000"

install:
	poetry install

run:
	poetry run uvicorn $(APP_MODULE) \
		--reload \
		--host $(HOST) \
		--port $(PORT)

lint:
	poetry run flake8 .

fmt:
	poetry run black .

test:
	poetry run pytest -v

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache