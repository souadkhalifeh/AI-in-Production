import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://iris_app:iris_test_password@127.0.0.1:5433/iris_test"
)

# Point the app at the test database before it is imported,
# so tests never touch the real database from .env
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.db.models import Base  # noqa: E402
from app.main import app  # noqa: E402

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)


@pytest.fixture(scope="session")
def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def clean_database(request):
    if request.node.get_closest_marker("integration") is None:
        yield
        return

    request.getfixturevalue("create_tables")

    table_names = ", ".join(
        table.name for table in Base.metadata.sorted_tables
    )
    with engine.begin() as connection:
        connection.execute(
            text(f"TRUNCATE {table_names} RESTART IDENTITY CASCADE")
        )
    yield


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
