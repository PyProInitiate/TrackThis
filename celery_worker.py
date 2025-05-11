import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL is None:
    raise ValueError("REDIS_URL environment variable not set.")

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)


@celery.task  # type: Callable[[str], None]
def run_task(task_id: str):
    """Run a task with the given task ID.

    Parameters
    ----------
    task_id : str
        The ID of the task to run.

    """
    # Simulate running a task
    print(f"Running task {task_id}")
