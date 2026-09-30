from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db

from app.models.recommendation import RecommendationHistory
from app.models.user import User


router = APIRouter(
    prefix="/api",
    tags=["History"],
)


@router.get("/history")
def history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    rows = db.scalars(
        select(RecommendationHistory)
        .where(
            RecommendationHistory.user_id == user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
    ).all()

    return [
        {
            "id": row.id,
            "planner_type": row.planner_type,
            "budget": row.budget,
            "request_data": row.request_data,
            "result_data": row.result_data,
            "ai_source": row.ai_source,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]


@router.get(
    "/recommendations-details/{recommendation_id}"
)
def recommendation_details(
    recommendation_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    row = db.scalar(
        select(RecommendationHistory).where(
            RecommendationHistory.id == recommendation_id,
            RecommendationHistory.user_id == user.id,
        )
    )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return {
        "id": row.id,
        "planner_type": row.planner_type,
        "budget": row.budget,
        "request_data": row.request_data,
        "result_data": row.result_data,
        "ai_source": row.ai_source,
        "created_at": row.created_at.isoformat(),
    }