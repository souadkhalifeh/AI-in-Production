from pydantic import BaseModel,Field, ConfigDict
from datetime import datetime

class PredictionRequest(BaseModel):
    user_id :int = Field(gt=0)
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)

class PredictionResponse(BaseModel):
    id: int
    prediction: str
    class_id: int
    user_id: int
    model_version: str


class PredictionHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    model_id: int
    predicted_class: str
    class_id: int
    created_at: datetime