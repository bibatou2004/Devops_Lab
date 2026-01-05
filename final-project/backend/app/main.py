from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging

from database import Base, Task
from schemas import TaskCreate, TaskUpdate, TaskResponse
from crud import (
    get_tasks,
    get_task,
    create_task,
    update_task,
    delete_task
)

# Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/devops_db"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="DevOps Data Pipeline API",
    description="Full-stack CRUD application for final project",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================
# Routes
# ============================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "backend",
        "database": "connected"
    }

@app.get("/tasks", response_model=list[TaskResponse], tags=["Tasks"])
async def list_tasks(db = None):
    """Get all tasks"""
    db = SessionLocal()
    try:
        tasks = get_tasks(db)
        return tasks
    finally:
        db.close()

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def read_task(task_id: int):
    """Get a specific task"""
    db = SessionLocal()
    try:
        task = get_task(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    finally:
        db.close()

@app.post("/tasks", response_model=TaskResponse, tags=["Tasks"])
async def create_new_task(task: TaskCreate):
    """Create a new task"""
    db = SessionLocal()
    try:
        return create_task(db, task)
    finally:
        db.close()

@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_existing_task(task_id: int, task_update: TaskUpdate):
    """Update a task"""
    db = SessionLocal()
    try:
        task = get_task(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return update_task(db, task, task_update)
    finally:
        db.close()

@app.delete("/tasks/{task_id}", tags=["Tasks"])
async def delete_existing_task(task_id: int):
    """Delete a task"""
    db = SessionLocal()
    try:
        task = get_task(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        delete_task(db, task)
        return {"message": "Task deleted successfully"}
    finally:
        db.close()

@app.get("/stats", tags=["Statistics"])
async def get_statistics():
    """Get statistics about tasks"""
    db = SessionLocal()
    try:
        tasks = get_tasks(db)
        completed = len([t for t in tasks if t.completed])
        total = len(tasks)
        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": total - completed,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
