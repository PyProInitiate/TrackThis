import datetime
import os
import random
import sys
from uuid import uuid4

import redis
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Process as ProcessModel
from schemas import Process as SchemaProcess
from utils import random_date, shuffle_files

sys.path.insert(0, "./models")
sys.path.insert(0, "./schemas")
sys.path.insert(0, "./utils")
sys.path.insert(0, "./database")
sys.path.insert(0, "./celery_worker")
sys.path.insert(0, "./__init__")
sys.path.insert(0, "./main")
sys.path.insert(0, "./polars_app")


POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://postgres:{POSTGRES_PASSWORD}@db:5433/taskmanager"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


load_dotenv(".venv")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URL)

# Initialize Redis connection
# Ensure the Redis connection is established correctly
r = redis.Redis(
    host="redis-17879.c90.us-east-1-3.ec2.redns.redis-cloud.com",
    port=17879,
    decode_responses=True,
    password=REDIS_PASSWORD,
)

success = r.set("foo", "bar")
# True

result = r.get("foo")
print(result)
# >>> bar


class Process(BaseModel):
    """Represents a process with various attributes and metadata.

    Attributes:
        id (str): A unique identifier for the process, generated using UUID.
        name (str | None): The name of the process. Optional.
        file_type (list[str]): A list of file types associated with
            the process,
            generated using the `shuffle_files` function.
        description (str | None): A description of the process. Optional.
        Location (str): The location of the process, randomly chosen from the
            current directory's contents.
        process_size (int | None): The size of the process, randomly generated
            between 1 and 100. Optional.
        process_size_on_disk (int): The size of the process on disk, randomly
            generated between 1 and 100. This ensures that the date is
            randomized within the specified range.
        Created_On (datetime.date): The creation date of the process, generated
            using the `random_date` function.
        Modified_On (datetime.date): The last modified date of the process,
            generated using the `random_date` function. This ensures that
            the date is randomized within the specified range.
        Accessed_On (datetime.date): The last accessed date of the process,
        generated using the `random_date` function.
        generated using the `random_date` function.
        Attributes (str): The attributes of the process, randomly chosen
            between "Read-Only" and "Hidden".
        CPU_task_size (int | None): The CPU task size of the process, randomly
            generated between 1 and 100.
            Optional.
        Memory_task_size (int | None): The memory task size of the process,
            randomly generated between 1 and 100. Optional.
        Disk_task_size (int | None): The disk task size of the process,
            randomly generated between 1 and 100. Optional.
        Network_task_size (int | None): The network task size of the process,
            randomly generated between 1 and 100. Optional.

    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str | None
    file_type: list[str] = Field(default_factory=shuffle_files)
    description: str | None
    Location: str = Field(default_factory=lambda: random.choice(os.listdir()))
    process_size: int | None = Field(
        default_factory=lambda: random.randint(1, sys.maxsize)
    )
    process_size_on_disk: int = Field(
        default_factory=lambda: random.randint(1, sys.maxsize)
    )
    Created_On: datetime.date = Field(default_factory=random_date)
    Modified_On: datetime.date = Field(default_factory=random_date)
    Accessed_On: datetime.date = Field(default_factory=random_date)
    Attributes: str = Field(
        default_factory=lambda: random.choice(["Read-Only", "Hidden"])
    )
    CPU_task_size: int | None = Field(
        default_factory=lambda: random.randint(1, 100)
    )
    Memory_task_size: int | None = Field(
        default_factory=lambda: random.randint(1, 100)
    )
    Disk_task_size: int | None = Field(
        default_factory=lambda: random.randint(1, 100)
    )
    Network_task_size: int | None = Field(
        default_factory=lambda: random.randint(1, 100)
    )


@app.post("/tasks", response_model=Process)
async def task(task: SchemaProcess) -> dict[str, str | int | bool | None]:
    """Create a new task with the given data.

    Parameters
    ----------
    task : Process
        The process data to create a new task.

    Returns
    -------
    dict[str, str | int | bool | None]
        A dictionary containing the task ID and process data or an error
        message if the task already exists.

    """
    cached_task = r.get(task.id)
    if cached_task:
        return {
            "error": "Task already exists",
            "status_code": 409,
            "task_id": task.id,
        }
    # Check if the task already exists in the database
    db_task = db.session.query(ProcessModel).filter_by(id=task.id).first()
    if db_task:
        return {
            "error": "Task already exists",
            "status_code": 409,
            "task_id": task.id,
        }
    # Create a new task if it doesn't exist

    """Create a new task with the given data.

    Parameters
    ----------
    task : Process
        The process data to create a new task.

    Returns
    -------
    dict[str, str | int | bool | None]
        A dictionary containing the task ID and process data.

    """
    db_task = ProcessModel(
        id=task.id, name=task.name, description=task.description
    )
    db.session.add(db_task)
    db.session.commit()  # Commit the changes to the database
    db.session.refresh(db_task)  # Refresh the session to get the latest data
    r.set(task.id, task.model_dump_json())  # Cache the task in Redis
    return db_task
    #


@app.post("tasks/stop/{id}", response_model=Process)
async def run_task(id: str) -> dict[str, str | int | bool | None]:
    """Stop a task by its ID.

    Parameters
    ----------
    id : str
        The ID of the task to stop.

    Returns
    -------
    dict[str, str | int | bool | None]
        A dictionary containing the task ID and process data or an error
        message if the task is not found.

    """
    task = r.get(id)
    if task:
        task_data = r.get(id)  # Retrieve the task data from Redis
        if task_data:
            task_dict = eval(task_data)  # Convert the string to a dictionary
            r.shutdown(task_dict.get("id"))  # Use the "id" from the dictionary
            return {"message": "Task stopped successfully", "task_id": id}
    return {"error": "Task not found", "status_code": 404, "task_id": id}


@app.get("/tasks")
async def get_tasks() -> list[Process]:
    """Retrieve a list of all tasks.

    Returns
    -------
    list[Process]
        A list of all process items.

    """
    r.get("tasks")
    tasks: list[Process] = []
    for key in r.scan_iter():
        task_data = r.get(key)
        if task_data:
            task_dict = eval(task_data)
            tasks.append(Process(**task_dict))
    return tasks


@app.get("/tasks/{id}")
async def get_task(id: str) -> Process | None:
    """Retrieve a task by its ID.

    Parameters
    ----------
    id : str
        The ID of the task to retrieve.

    Returns
    -------
    Process
        The process item with the specified ID.

    """
    task_data = r.get(id)
    return Process(**eval(task_data)) if task_data else None


@app.put("/tasks/{id}", response_model=Process)
async def tasks(tasks: SchemaProcess) -> dict[str, str | int | bool | None]:
    """Update a task by its ID.

    Parameters
    ----------
    id : str
        The ID of the task to update.
    tasks : Process
        The updated process data.

    Returns
    -------
    dict[str, str | int | bool | None]
        A dictionary containing the updated task ID and process data.

    """
    return {"task_id": tasks.id, **tasks.model_dump()}
