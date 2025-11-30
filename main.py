import asyncio
import datetime
import importlib
import os
import random
import sys
from uuid import uuid4

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
#from starlette_context import context
from starlette_context.middleware import RawContextMiddleware

from models import Base
from utils import random_date, shuffle_files

importlib.import_module("models.py")

importlib.import_module("polars_app.py")

app = FastAPI()
SessionLocal: async_sessionmaker[AsyncSession] | None = None

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    if SessionLocal is None:
        raise RuntimeError("SessionLocal is not initialized; call main() to initialize the engine")
    async with SessionLocal() as session:
        yield session



async def async_main() -> None:
    engine = create_async_engine(
        "postgresql://postgres:{POSTGRES_PASSWORD}@db:5433/taskmanager",
        connect_args={"check_same_thread": False},
        execution_options={"isolation_level": "REPEATABLE READ"},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # insert @functions here
    await engine.dispose()
asyncio.run(async_main())


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
    orm_mode = True

@app.post("/task", response_model=Process)
async def create_task(session: AsyncSession = Depends(get_async_session)):


@app.post("tasks/stop/{id}")
async def run_task(id: str):



@app.get("/tasks")
async def get_tasks(session: AsyncSession = Depends(get_async_session)):




@app.get("/tasks/{id}")
async def get_task(session: AsyncSession = Depends(get_async_session)):
    async with async__session() as session:
        get_task_id = await async_session.get(Process.id)




@app.put("/tasks/{id}", response_model=Process)
async def tasks(session: AsyncSession = Depends(get_async_session)):
