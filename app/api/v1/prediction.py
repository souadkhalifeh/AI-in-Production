from fastapi import APIRouter, HTTPException, Depends, Query
from app.utils.exception import ModelLoadError
from app.schemas.prediction import PredictionRequest, PredictionResponse, PredictionHistoryResponse
from app.services.model_service import predict
from app.utils.logger import get_logger

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Prediction, User, MLModel


logger = get_logger()
router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, status_code=201)
def make_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    user= db.get(User, request.user_id)
    
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    model = db.scalar(select(MLModel).where(MLModel.name =="iris_classifier", 
                                             MLModel.version=="1.0.0"))
    
    if model is None: 
        raise HTTPException(status_code=503, detail="Active model is not registered")
    
    features = [
        request.sepal_length,
        request.sepal_width,
        request.petal_length,
        request.petal_width
    ]

    result = predict(features)


    prediction_record = Prediction(
        user_id=user.id,
        model_id=model.id,
        sepal_length=request.sepal_length,
        sepal_width=request.sepal_width,
        petal_length=request.petal_length,
        petal_width=request.petal_width,
        predicted_class=result["prediction"],
        class_id=result["class_id"], 
        confidence=result["confidence"])

    db.add(prediction_record)

    try:
        db.commit()
        db.refresh(prediction_record)
    except Exception:
        db.rollback()
        raise

    return {
        "id": prediction_record.id,
        "prediction": prediction_record.predicted_class,
        "class_id": prediction_record.class_id,
        "user_id":prediction_record.user_id, 
        "model_version":model.version
    }

@router.get(
    "/predictions",
    response_model=list[PredictionHistoryResponse]
)
def get_predictions(
    user_id: int | None = Query(default=None, gt=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    statement = select(Prediction)

    if user_id is not None:
        statement = statement.where(
            Prediction.user_id == user_id
        )

    statement = (
        statement
        .order_by(Prediction.id.desc())
        .limit(limit)
    )

    return db.scalars(statement).all()