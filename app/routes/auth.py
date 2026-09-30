from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.dependencies import get_current_user
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.db.session import get_db

from app.models.recommendation import RecommendationHistory
from app.models.schemas import (
    LoginRequest,
    RegisterRequest,
    UserOut,
)
from app.models.user import User


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)

settings = get_settings()


@router.post(
    "/register",
    response_model=UserOut,
    status_code=201,
)
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
):

    email = payload.email.lower().strip()

    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )

    return user


@router.post(
    "/login",
    response_model=UserOut,
)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):

    email = payload.email.lower().strip()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user or not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.id)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )

    return user


@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        key="access_token"
    )

    return {
        "message": "Logged out successfully"
    }


@router.get("/session-info")
def session_info(
    user: User = Depends(get_current_user),
):

    return {
        "logged_in": True,
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
    }


@router.get("/session-data")
def session_data(
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
        .limit(5)
    ).all()

    return {
        "user": UserOut.model_validate(user),
        "recent_count": len(rows),
        "recent": [
            {
                "id": row.id,
                "planner_type": row.planner_type,
                "budget": row.budget,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ],
    }