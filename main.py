from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import parse_qs
import sqlite3

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "focus.db"
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PRIORITIES = {"High", "Medium", "Low"}


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL CHECK (priority IN ('High', 'Medium', 'Low')),
                completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1)),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="Daily Focus Board", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@app.get("/")
async def index(request: Request):
    with get_connection() as connection:
        tasks = connection.execute(
            "SELECT id, title, priority, completed FROM tasks "
            "ORDER BY completed ASC, id DESC"
        ).fetchall()

    total = len(tasks)
    completed_count = sum(task["completed"] for task in tasks)
    progress = round(completed_count / total * 100) if total else 0

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tasks": tasks,
            "total": total,
            "completed_count": completed_count,
            "progress": progress,
            "all_complete": total > 0 and completed_count == total,
        },
    )


@app.post("/tasks")
async def create_task(request: Request):
    form = parse_qs((await request.body()).decode("utf-8"), keep_blank_values=True)
    title = form.get("title", [""])[0].strip()
    priority = form.get("priority", ["Medium"])[0]

    if title and priority in PRIORITIES:
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO tasks (title, priority) VALUES (?, ?)",
                (title[:200], priority),
            )

    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/toggle")
async def toggle_task(task_id: int):
    with get_connection() as connection:
        connection.execute(
            "UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END "
            "WHERE id = ?",
            (task_id,),
        )
    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/delete")
async def delete_task(task_id: int):
    with get_connection() as connection:
        connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return RedirectResponse(url="/", status_code=303)
