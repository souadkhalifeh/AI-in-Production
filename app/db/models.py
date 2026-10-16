from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    predictions: Mapped[list["Prediction"]] = relationship(
        back_populates="user"
    )


class MLModel(Base):
    __tablename__ = "ml_models"

    __table_args__ = (
        UniqueConstraint(
            "name", "version", name="uq_model_version"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(String(100))
    version: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    predictions: Mapped[list["Prediction"]] = relationship(
        back_populates="model"
    )


class Prediction(Base):
    __tablename__ = "predictions"

    __table_args__ = (
        CheckConstraint(
            "sepal_length > 0", name="positive_sepal_length"
        ),
        CheckConstraint(
            "sepal_width > 0", name="positive_sepal_width"
        ),
        CheckConstraint(
            "petal_length > 0", name="positive_petal_length"
        ),
        CheckConstraint(
            "petal_width > 0", name="positive_petal_width"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    model_id: Mapped[int] = mapped_column(
        ForeignKey("ml_models.id")
    )

    sepal_length: Mapped[float] = mapped_column(Float)
    sepal_width: Mapped[float] = mapped_column(Float)
    petal_length: Mapped[float] = mapped_column(Float)
    petal_width: Mapped[float] = mapped_column(Float)

    predicted_class: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    confidence: Mapped[float | None] = mapped_column(
    Float,
    nullable=True
)

    user: Mapped["User"] = relationship(
        back_populates="predictions"
    )
    model: Mapped["MLModel"] = relationship(
        back_populates="predictions"
    )
    feedback: Mapped["Feedback | None"] = relationship(
        back_populates="prediction",
        uselist=False
    )


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    prediction_id: Mapped[int] = mapped_column(
        ForeignKey("predictions.id"), unique=True
    )
    is_correct: Mapped[bool] = mapped_column(Boolean)
    comment: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    prediction: Mapped["Prediction"] = relationship(
        back_populates="feedback"
    )