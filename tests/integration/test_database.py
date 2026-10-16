import pytest
from sqlalchemy import select

from app.db.models import User


@pytest.mark.integration
def test_create_user(client, db_session):
    response = client.post(
        "/api/v1/users",
        json={
            "name": "Sara",
            "email": "sara@example.com"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Sara"
    assert data["email"] == "sara@example.com"
    assert "id" in data

    saved_user = db_session.scalar(
        select(User).where(
            User.email == "sara@example.com"
        )
    )

    assert saved_user is not None
    assert saved_user.name == "Sara"


@pytest.mark.integration
def test_duplicate_user_email(client):
    user_data = {
        "name": "Sara",
        "email": "sara@example.com"
    }

    first_response = client.post(
        "/api/v1/users",
        json=user_data
    )

    second_response = client.post(
        "/api/v1/users",
        json=user_data
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409