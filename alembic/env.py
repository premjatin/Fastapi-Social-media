from logging.config import fileConfig
import os 

from sqlalchemy import engine_from_config, pool, create_engine

from app.models import Base
from alembic import context

db_user = os.environ.get("DATABASE_USERNAME")
db_pass = os.environ.get("DATABASE_PASSWORD")
db_host = os.environ.get("DATABASE_HOSTNAME")
db_port = os.environ.get("DATABASE_PORT")
db_name = os.environ.get("DATABASE_NAME")

if not all([db_user, db_pass, db_host, db_port, db_name]):
    raise RuntimeError("One or more database environment variables are not set!")

final_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?sslmode=require"

config = context.config

config.set_main_option("sqlalchemy.url", final_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


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
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()