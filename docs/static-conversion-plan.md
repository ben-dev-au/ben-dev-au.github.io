# Plan: Convert Dynamic FastAPI Site to Static GitHub Pages Site

## Context

The portfolio site at ben-dev.au is currently a FastAPI + SQLite application deployed to Heroku. The database only holds 3 hardcoded projects (seeded via script), the contact form is an Airtable embed (already external), and there's no server-side logic that couldn't be replaced with static HTML. Converting to a static site enables free hosting on GitHub Pages and eliminates unnecessary infrastructure.

## Approach

Flatten all Jinja2 templates into a single `index.html` with project data inlined, move static assets to root-level `static/`, and remove all Python backend code.

## Steps

### 1. Create static `index.html` at project root

Build by manually inlining all content from the Jinja2 templates:

- Start from `frontend/templates/homepage/index.html`
- Replace each `{% include 'components/X.html' %}` with the literal content of that component
- For resume component, also inline the nested `{% include 'resume/resume.html' %}`
- Replace all `{{ url_for('static', path='/css/X.css') }}` with `/static/css/X.css` (and same for JS)
- Change `href="/static/favicon.svg"` to `href="/favicon.svg"` (favicons are at root)
- Render the `projects.html` Jinja2 logic into static HTML using the seed data:
  - **Featured**: Priferral (with 5 tech badges, link to priferral.com)
  - **Card 1** (shadow-red): WordPress Store (no link)
  - **Card 2** (shadow-blue): Portfolio Website (link to ben-dev.au, update description/tech stack to reflect it's now a static site)

**Files to read**: All 7 component templates + `resume/resume.html` + `add_projects.py`

### 2. Move `frontend/static/` to root-level `static/`

```
mv frontend/static/ static/
```

All existing paths in CSS (`url("/static/images/...")`) and HTML (`src="/static/images/..."`) use absolute `/static/...` paths, which resolve correctly from GitHub Pages root with a custom domain. No path changes needed in CSS or JS files.

### 3. Verify locally

```
python3 -m http.server 8000
```

Check: all sections render, images load, Swiper timeline works, polaroid gallery works, scroll navigation works.

### 4. Delete backend and Python infrastructure

Remove from git tracking:
- `backend/` (entire directory)
- `portfolio.db`
- `pyproject.toml`, `poetry.lock`, `.python-version`
- `Procfile`
- `frontend/` (entire directory — content has been moved/inlined)
- `tests/`
- `makefile`

### 5. Update config files

**`.gitignore`** — Simplify to:
```
.DS_Store
.idea/
*.log
.env
dev_notes.md
.playwright-mcp/
```

**`CLAUDE.md`** — Rewrite for static site (no backend, no database, `python3 -m http.server` for local dev, deploy via GitHub Pages push to main).

**`CNAME`** — Keep as-is (`ben-dev.au`).

### 6. Add optional `makefile` for local dev

Single `serve` target: `python3 -m http.server 8000`

## Critical Files

| File | Role |
|------|------|
| `frontend/templates/homepage/index.html` | Main template skeleton |
| `frontend/templates/components/*.html` (7 files) | Content to inline |
| `frontend/templates/resume/resume.html` | Nested include in resume component |
| `frontend/templates/components/projects.html` | Only template with DB-driven logic |
| `backend/add_projects.py` | Source of truth for project data to inline |
| `frontend/static/css/base.css` | Has `/static/images/grunge.png` path refs |
| `frontend/static/css/intro.css` | Has `/static/images/somm_laptop_cellar.jpeg` path ref |

## Verification

1. Run `python3 -m http.server 8000` from project root
2. Open `http://localhost:8000` and verify:
   - All 7 sections render (navbar, intro, about, resume/timeline, projects, contact, scroll-top)
   - All images load (intro background, 6 about photos, 3 project images, grunge stamp mask)
   - Swiper timeline carousel slides and pagination dots work
   - Polaroid gallery drag + lightbox work
   - Keyboard arrow navigation works
   - Mobile responsive layout works
   - Airtable contact form loads in iframe
   - "Under Casual Development" stamp renders with grunge mask
3. Verify no 404s in browser dev tools Network tab
