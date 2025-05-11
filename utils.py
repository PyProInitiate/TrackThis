import datetime
import os
import random


def random_date():
    """Generate a random date between 2000-01-01 and 2023-10-01."""
    start_date = datetime.date(1984, 8, 14)
    end_date = datetime.date(2025, 4, 27)
    return start_date + datetime.timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )


def shuffle_files():
    """Generate a random file type."""
    files = os.listdir("file_types")
    random.shuffle(files)
    return files
