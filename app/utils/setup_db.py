import subprocess

from sqlalchemy import create_engine, text

from app.core.config import settings


def create_database():
    engine = create_engine(f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}")

    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")

        # Check if database exists
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{settings.POSTGRES_DB}'"))
        if not result.fetchone():
            # Create database if it doesn't exist
            conn.execute(text(f"CREATE DATABASE {settings.POSTGRES_DB}"))
            print(f"Database {settings.POSTGRES_DB} created")
        else:
            print(f"Database {settings.POSTGRES_DB} already exists")

if __name__ == "__main__":
    create_database()
    # Run migrations after database is created
    subprocess.run(["alembic", "upgrade", "head"])