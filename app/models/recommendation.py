from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class RecommendationHistory(Base):

    __tablename__ = "recommendation_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    planner_type: Mapped[str] = mapped_column(
        String(30),
        index=True,
        nullable=False,
    )

    budget: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    request_data: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    result_data: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    ai_source: Mapped[str] = mapped_column(
        String(30),
        default="fallback",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )