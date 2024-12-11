import logging
import os
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent
parent_dir = str(current_dir.parent)
sys.path.append(parent_dir)

from alembic.config import Config
from alembic import command
from src.database.session import engine
from src.database.models import Base
from src.database.create_db import create_database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def init_db():
    """Initialize the database and create all tables."""
    try:
        # Create database if it doesn't exist
        create_database()

        # Only run Alembic migrations (remove Base.metadata.create_all)
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_db()
