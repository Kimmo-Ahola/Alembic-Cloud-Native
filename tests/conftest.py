import os
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from alembic.config import Config
from alembic import command

import app.model
from app.main import app
from app.database import get_db

TEST_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+psycopg2://tasks:tasks@localhost:5433/tasks_test"
)

engine = create_engine(url=TEST_URL)
TestingSession = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", TEST_URL)
    # kör alla migrationer från base till head
    command.upgrade(cfg, "head") # alembic upgrade head
    yield


@pytest.fixture(autouse=True)
def clean_tables():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE TASKS"))


# skriver över get_db med en ny
# TestingSession
@pytest.fixture
def client():
    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
