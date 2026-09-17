import os
import sys
from logging.config import fileConfig

from sqlalchemy import text
from alembic import context

# 1. Project Root Path-ஐ Sys Path-இல் சேர்க்கவும்
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Database connection மற்றும் Models-ஐ Import செய்தல்
from app.database.connection import Base, engine, DATABASE_URL
from app.models.book import Book
from app.models.category import Category
from app.models.author import Author
from app.models.borrow import Borrow
from app.models.member import Member

config = context.config

# Logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Model Metadata-வை Alembic உடன் இணைத்தல்
target_metadata = Base.metadata

# Database URL-இல் '%' இருந்தால் வரும் பிழையைத் தவிர்க்க (URL Escape Handle)
if DATABASE_URL:
    url_str = str(DATABASE_URL)
    config.set_main_option("sqlalchemy.url", url_str.replace("%", "%%"))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine  # connection.py-இல் உள்ள engine-ஐப் பயன்படுத்துகிறது

    with connectable.connect() as connection:
        # Foreign key error வராமல் இருக்க தற்காலிகமாக FK Check-ஐ Off செய்கிறது
        connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))

        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()