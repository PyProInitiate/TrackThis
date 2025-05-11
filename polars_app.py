import asyncio

import polars as pl
from fastapi import FastAPI
from great_tables import loc, style

# Load environment variables
app = FastAPI()


@app.get("/tasks")
async def get_tasks():
    """Retrieve a sample DataFrame containing task information.

    Returns
    -------
    pl.DataFrame
        A DataFrame with sample rows and columns data.

    """
    return pl.DataFrame(
        {
            "rows": [2],
            "cols": [14],
        }
    )


async def process_data(df: pl.DataFrame) -> pl.DataFrame:
    """Process the given DataFrame by casting columns to Int32.

    Parameters
    ----------
    df : pl.DataFrame
        The input DataFrame to process.

    Returns
    -------
    pl.DataFrame
        The processed DataFrame with columns cast to Int32.

    """
    # Simulate some processing
    await asyncio.sleep(1)
    df.style.tab_header(
        title="Task Manager", subtitle="Simulated Task Manager"
    )
    return df.with_columns(
        [
            pl.col("rows").cast(pl.Int32),
            pl.col("cols").cast(pl.Int32),
        ]
    )


async def get_processed_tasks():
    """Retrieve a sample DataFrame containing processed task information.

    Returns
    -------
    dict
        A dictionary containing processed data.

    """
    df = pl.DataFrame(
        {
            "rows": [2],
            "cols": [14],
        }
    )
    df.style.tab_style(
        style.fill("blue"),
        loc.body(
            rows=pl.col("rows") == pl.col("cols"),
        ),
    )
    df.style.tab_style(
        style.fill("dark blue"),
        loc.body(
            rows=pl.col("rows") == pl.col("row").max(),
        ),
    )
    processed_data = await process_data(df)
    return {"data": processed_data}
