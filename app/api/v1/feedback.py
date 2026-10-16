from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Feedback, Prediction
from app.schemas.feedback import FeedbackCreate, FeedbackResponse


router = APIRouter()


@router.post(
    "/predictions/{prediction_id}/feedback",
    response_model=FeedbackResponse,
    status_code=201
)
def submit_feedback(
    prediction_id: int,
    request: FeedbackCreate,
    db: Session = Depends(get_db)
):
    prediction = db.get(Prediction, prediction_id)

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found."
        )

    feedback = Feedback(
        prediction_id=prediction_id,
        is_correct=request.is_correct,
        comment=request.comment
    )

    db.add(feedback)

    try:
        db.commit()
        db.refresh(feedback)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Feedback already exists for this prediction."
        )

    return feedback