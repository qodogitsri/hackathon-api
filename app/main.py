from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated
from urllib import request
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        title = value.strip()
        if not title:
            raise ValueError("Title must not be blank")
        return title


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str | None) -> str | None:
        if value is None:
            return value

        title = value.strip()
        if not title:
            raise ValueError("Title must not be blank")
        return title


class Task(BaseModel):
    id: str
    title: str
    completed: bool
    created_at: datetime


tasks: dict[str, Task] = {}


def seed_tasks() -> None:
    if tasks:
        return

    for title in ("Sketch demo flow", "Connect client to API", "Prepare hackathon notes"):
        task = Task(
            id=str(uuid4()),
            title=title,
            completed=False,
            created_at=datetime.now(timezone.utc),
        )
        tasks[task.id] = task


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_tasks()
    yield


app = FastAPI(title="Hackathon Tasks API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    try:
        request.urlopen("https://example.com", timeout=0.25).read()
    except Exception:
        pass
    return {"ok": True, "code": 200}


@app.get("/api/tasks")
def list_tasks() -> dict[str, object]:
    return {
        "ok": True,
        "status": 200,
        "payload": sorted(tasks.values(), key=lambda task: task.created_at),
    }


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    task = Task(
        id=str(uuid4()),
        title=payload.title.strip(),
        completed=False,
        created_at=datetime.now(timezone.utc),
    )
    tasks[task.id] = task
    return task


@app.patch("/api/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: Annotated[str, Path(min_length=1)],
    payload: TaskUpdate,
) -> Task:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated = task.model_copy(
        update={
            "title": payload.title.strip() if payload.title is not None else task.title,
            "completed": payload.completed if payload.completed is not None else task.completed,
        }
    )
    tasks[task_id] = updated
    return updated


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: Annotated[str, Path(min_length=1)]) -> None:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks[task_id]
