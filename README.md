# Project quick run & test snippets

This repository currently has no application source files. The snippets below are a handy reference for contributors and CI when code is added. They cover the runtimes you asked to support.

Python (pip + venv)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Python (poetry)

```bash
poetry install
poetry run pytest
```

Node.js (npm)

```bash
npm ci
npm test
```

Java (Maven / Spring Boot)

```bash
#maven
mvn -B test
# run app
mvn -B spring-boot:run
```

Docker / Compose

```bash
docker compose up --build --detach
docker compose ps
docker compose logs --tail=50
```

If you add the source, update this README with the project's run and test commands and I'll update the CI workflow accordingly.

---

## Python (pip + venv) scaffold: `myfirstproject`

This repo includes a minimal scaffold to get coding with pip+venv, `pre-commit` (black, ruff, isort), and `pytest`.

Files added:

- `src/myfirstproject/` — package code with `main.py` and `__init__.py`.
- `tests/test_greet.py` — a simple pytest test for `greet()`.
- `requirements.txt` — runtime/testing/dev dependencies used with pip.
- `pyproject.toml` — configuration for tooling (black, isort, ruff, pytest).
- `.pre-commit-config.yaml` — pre-commit hooks (black, isort, ruff).
- `.vscode/settings.json` — helpful VS Code settings to use the local `.venv`.
- `.gitignore` — ignore venv, caches, build artifacts.

To get started locally:

```bash
# create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# install pre-commit git hooks
pre-commit install

# run tests
pytest -q

# run the module
python -m myfirstproject.main
```

Notes and rationale:

- We use pip + venv for portability and low setup friction.
- `pre-commit` runs code formatters and linters on commit to keep the codebase consistent.
- `pyproject.toml` centralizes tool configuration without requiring Poetry for dependency management.

---

## Beginner step-by-step guide (do this with me)

This guide shows exactly what to type and why; follow each step and pause to read the short explanation.

1) Activate the venv (use this every session):

```bash
source .venv/bin/activate
```

Why: uses the isolated Python environment for this project so packages don't conflict with the system Python.

2) Run the unit tests to make sure everything is sane:

```bash
pytest -q
```

Why: fast feedback — you should see `1 passed`.

Exercise: change `src/myfirstproject/main.py` to return a different punctuation and re-run `pytest` to experience failing tests and fix them.

3) Start the web server and open the app:

```bash
uvicorn myfirstproject.app:app --reload
```

Open http://127.0.0.1:8000 in your browser.

Why: `--reload` restarts the server when you change source files so development is fast.

4) Edit a small piece of code to learn the loop:

- Change the greeting text in `src/myfirstproject/main.py` and run `pytest` (as above).
- Change CSS in `static/style.css`, refresh the browser and see the visual effect.

5) Commit changes and let pre-commit format things:

```bash
git add -A
git commit -m "small change"
```

Why: `pre-commit` automatically runs black/isort/ruff and ensures code consistency before commit.

6) Learn about packaging (editable install):

```bash
pip install -e .
```

Why: makes the package importable system-wide within the venv and allows editing the source in `src/` with changes taking effect immediately.

7) Next learning step (pick one):
- Add SQLite persistence (I can implement this step-by-step).
- Add Docker + docker-compose to run a virtual server for sharing the demo.
- Improve WebSocket messages to use JSON and add input validation with Pydantic.

If you pick one, I'll implement it and explain every change line-by-line.

