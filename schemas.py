import datetime
import os
import random
from uuid import uuid4

from pydantic import BaseModel, Field

from utils import random_date, shuffle_files


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

    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str | None = None
    file_type: list[str] = Field(default_factory=shuffle_files)
    description: str | None = None
    Location: str = os.getcwd()
    process_size: int | None = Field(
        default_factory=lambda: random.randint(1, 100)
    )
    process_size_on_disk: int = Field(
        default_factory=lambda: random.randint(1, 100)
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

    class Config:
        """Configuration class for enabling ORM mode in the Pydantic model."""

        orm_mode = True
