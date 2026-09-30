from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class RegisterRequest(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    email: EmailStr


class HomeRequest(BaseModel):

    budget: int = Field(
        gt=0,
        le=10_000_000,
    )

    rooms: list[str] = Field(
        min_length=1,
    )

    style: str = Field(
        default="Modern",
        max_length=80,
    )

    city: str = Field(
        default="Vellore",
        max_length=100,
    )

    notes: str = Field(
        default="",
        max_length=1000,
    )


class PartyRequest(BaseModel):

    budget: int = Field(
        gt=0,
        le=10_000_000,
    )

    guests: int = Field(
        gt=0,
        le=10_000,
    )

    event_type: str = Field(
        default="Birthday",
        max_length=80,
    )

    venue: str = Field(
        default="Indoor",
        max_length=120,
    )

    city: str = Field(
        default="Vellore",
        max_length=100,
    )

    notes: str = Field(
        default="",
        max_length=1000,
    )


class JewelryRequest(BaseModel):

    budget: int = Field(
        gt=0,
        le=10_000_000,
    )

    occasion: str = Field(
        default="Wedding",
        max_length=80,
    )

    style: str = Field(
        default="Elegant",
        max_length=80,
    )

    outfit_color: str = Field(
        default="Not specified",
        max_length=80,
    )

    notes: str = Field(
        default="",
        max_length=1000,
    )


class RecommendationResponse(BaseModel):

    id: int | None = None

    planner_type: str

    budget: int

    summary: str

    allocations: list[dict]

    recommendations: list[dict]

    tips: list[str]

    ai_source: str