import pytest
from pydantic import ValidationError

from app.schemas.prediction import PredictionRequest


@pytest.mark.unit
def test_valid_prediction_input():
    request = PredictionRequest(
        user_id=1,
        sepal_length=5.1,
        sepal_width=3.5,
        petal_length=1.4,
        petal_width=0.2
    )

    assert request.sepal_length == 5.1
    assert request.user_id == 1


@pytest.mark.unit
def test_negative_sepal_length_is_rejected():
    with pytest.raises(ValidationError):
        PredictionRequest(
            user_id=1,
            sepal_length=-5.1,
            sepal_width=3.5,
            petal_length=1.4,
            petal_width=0.2
        )


@pytest.mark.unit
def test_missing_feature_is_rejected():
    with pytest.raises(ValidationError):
        PredictionRequest(
            user_id=1,
            sepal_length=5.1,
            sepal_width=3.5,
            petal_length=1.4
        )