import asyncio

import polars as pl
from fastapi import FastAPI
from great_tables import loc, style

# Load environment variables
app = FastAPI()


@app.get("/tasks")
async def get_tasks():



async def process_data(df: pl.DataFrame) -> pl.DataFrame:


async def get_processed_tasks():
