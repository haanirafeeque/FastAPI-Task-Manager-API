import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def init_database():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            # Create the tasks table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)

            # Check whether the table is empty
            cur.execute("SELECT COUNT(*) FROM tasks")
            count = cur.fetchone()[0]

            # Insert the three example tasks only on first run
            if count == 0:
                cur.executemany(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (%s, %s)
                    """,
                    [
                        ("Buy groceries", False),
                        ("Complete FastAPI assignment", False),
                        ("Read PostgreSQL documentation", True),
                    ],
                )

        conn.commit()