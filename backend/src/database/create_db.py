import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


def create_database():
    """Create the database if it doesn't exist."""

    # Parse DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    parsed = urlparse(db_url)
    db_name = parsed.path[1:]  # Remove leading '/'

    # Connect to PostgreSQL server (not the database)
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        user=parsed.username,
        password=parsed.password,
        database="postgres"  # Connect to default postgres database
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    try:
        # Check if database exists
        cursor.execute(
            f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            # Create database
            cursor.execute(f'CREATE DATABASE {db_name}')
            logger.info(f"Database {db_name} created successfully!")
        else:
            logger.info(f"Database {db_name} already exists.")

    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    create_database()
