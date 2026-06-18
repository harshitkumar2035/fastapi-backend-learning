from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from pydantic import BaseModel
import logging 
import sys
import time
from typing import List


# ------ Logging -----
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]

)
logger = logging.getLogger(__name__)



# ------ FastAPI App -----
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)


# ----- CORS ------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Request logging middleware -----
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response

# ----- Error handlers -----
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error."})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# ---------- Aapke original endpoints (same hain) ----------
class User(BaseModel):
    name: str
    age: int

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

tasks_db = [
    Task(id=1, title="Buy groceries"),
    Task(id=2, title="Read a book"),
    Task(id=3, title="Write unit tests", completed=True),
]

@app.get("/")
def home():
    logger.info("Home endpoint called")
    return {"message": "Hello from Python API server!"}

@app.post("/user")
def create_user(user: User):
    logger.info(f"User created: {user.name}, age {user.age}")
    return {"msg": "User created successfully", "user": user}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    
    raise HTTPException(status_code=404, detail="Task not found")
    

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            updated_task.id = task_id
            tasks_db[index] = updated_task
            return updated_task
    
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(index)
            return {"message": "Task deleted"}
    
    raise HTTPException(status_code=404, detail="Task not found")