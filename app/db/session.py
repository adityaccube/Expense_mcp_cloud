from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_NAME = "ExpenseTrackerMCP"

DATABASE_URL = (
    f"postgresql+psycopg2://postgres:1234@localhost:5432/{DATABASE_NAME}"
)

ADMIN_DATABASE_URL = (
    "postgresql+psycopg2://postgres:1234@localhost:5432/postgres"
)


def ensure_database():
    try:
        with create_engine(DATABASE_URL).connect():
            return
    except Exception:
        pass

    admin_engine = create_engine(
        ADMIN_DATABASE_URL,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with admin_engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT 1 FROM pg_database "
                    "WHERE datname = :database_name"
                ),
                {"database_name": DATABASE_NAME},
            ).scalar()

            if result is None:
                conn.execute(
                    text(f'CREATE DATABASE "{DATABASE_NAME}"')
                )
    finally:
        admin_engine.dispose()


ensure_database()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)