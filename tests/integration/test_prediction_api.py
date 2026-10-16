from unittest.mock import patch

import pytest

from app.db.models import MLModel


@pytest.mark.integration
def test_prediction_endpoint(client, db_session):
    # 1. Create a user
    user_response = client.post(
        "/api/v1/users",
        json={
            "name": "Omar",
            "email": "omar@example.com"
        }
    )

    assert user_response.status_code == 201

    user_id = user_response.json()["id"]
    model_id ='iris_classifier'

    # 2. Register the model
    ml_model = MLModel(
        name="iris_classifier",
        version="1.0.0",    )

    db_session.add(ml_model)
    db_session.commit()

    # 3. Mock the prediction function
    fake_prediction = {
        "prediction": "setosa",
        "class_id": 0,
        "confidence": 0.95
    }

    with patch(
        "app.api.v1.prediction.predict",
        return_value=fake_prediction
    ):
        response = client.post(
            "/api/v1/predict",
            json={
                "user_id": user_id,
                "model_id":model_id,
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        )

    assert response.status_code == 201

    data = response.json()

    assert data["prediction"] == "setosa"
    assert data["class_id"] == 0
    assert data["user_id"] == user_id
    assert "id" in data