from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.dependencies import get_current_user
from app.db.session import get_db

from app.models.recommendation import (
    RecommendationHistory,
)

from app.models.schemas import (
    HomeRequest,
    PartyRequest,
    RecommendationResponse,
)

from app.models.user import User

from app.services.gemini_service import (
    generate_recommendation,
)


router = APIRouter(
    prefix="/api",
    tags=["Planners"],
)


def save_history(
    db: Session,
    user: User,
    planner: str,
    data: dict,
    result: dict,
    source: str,
):

    row = RecommendationHistory(
        user_id=user.id,
        planner_type=planner,
        budget=int(data["budget"]),
        request_data=data,
        result_data=result,
        ai_source=source,
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return row


@router.post(
    "/generate-home",
    response_model=RecommendationResponse,
)
def generate_home(
    payload: HomeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    data = payload.model_dump()

    result, source = generate_recommendation(
        "home",
        data,
    )

    row = save_history(
        db,
        user,
        "home",
        data,
        result,
        source,
    )

    return {
        "id": row.id,
        "planner_type": "home",
        "budget": payload.budget,
        **result,
        "ai_source": source,
    }


@router.post(
    "/generate-party",
    response_model=RecommendationResponse,
)
def generate_party(
    payload: PartyRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    data = payload.model_dump()

    result, source = generate_recommendation(
        "party",
        data,
    )

    row = save_history(
        db,
        user,
        "party",
        data,
        result,
        source,
    )

    return {
        "id": row.id,
        "planner_type": "party",
        "budget": payload.budget,
        **result,
        "ai_source": source,
    }


@router.post(
    "/generate-jewelry",
    response_model=RecommendationResponse,
)
async def generate_jewelry(
    budget: int = Form(
        ...,
        gt=0,
        le=10_000_000,
    ),

    occasion: str = Form(
        "Wedding"
    ),

    style: str = Form(
        "Elegant"
    ),

    outfit_color: str = Form(
        "Not specified"
    ),

    notes: str = Form(
        ""
    ),

    outfit_image: UploadFile | None = File(
        default=None
    ),

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    if len(occasion) > 80:
        raise HTTPException(
            status_code=422,
            detail="Occasion is too long",
        )

    if len(style) > 80:
        raise HTTPException(
            status_code=422,
            detail="Style is too long",
        )

    if len(outfit_color) > 80:
        raise HTTPException(
            status_code=422,
            detail="Outfit color is too long",
        )

    if len(notes) > 1000:
        raise HTTPException(
            status_code=422,
            detail="Notes are too long",
        )

    image_bytes = None
    mime_type = None

    if (
        outfit_image
        and outfit_image.filename
    ):

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if (
            outfit_image.content_type
            not in allowed_types
        ):
            raise HTTPException(
                status_code=415,
                detail=(
                    "Only JPEG, PNG or WEBP "
                    "images are allowed"
                ),
            )

        image_bytes = await outfit_image.read()

        max_size = (
            get_settings().max_upload_mb
            * 1024
            * 1024
        )

        if len(image_bytes) > max_size:
            raise HTTPException(
                status_code=413,
                detail="Image is too large",
            )

        mime_type = (
            outfit_image.content_type
        )

    data = {
        "budget": budget,
        "occasion": occasion.strip(),
        "style": style.strip(),
        "outfit_color": outfit_color.strip(),
        "notes": notes.strip(),
        "image_supplied": bool(image_bytes),
    }

    result, source = generate_recommendation(
        "jewelry",
        data,
        image_bytes,
        mime_type,
    )

    row = save_history(
        db,
        user,
        "jewelry",
        data,
        result,
        source,
    )

    return {
        "id": row.id,
        "planner_type": "jewelry",
        "budget": budget,
        **result,
        "ai_source": source,
    }
    