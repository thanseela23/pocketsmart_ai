import json
import logging
from typing import Any

from app.core.config import get_settings
from app.services.catalog_service import catalog_for


logger = logging.getLogger(__name__)

settings = get_settings()


try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


def _fallback(
    planner: str,
    data: dict,
    image_supplied: bool = False,
) -> dict:

    budget = int(data["budget"])

    items = catalog_for(
        planner,
        budget,
    )

    if planner == "home":

        furniture = round(
            budget * 0.40
        )

        lighting = round(
            budget * 0.20
        )

        decor = round(
            budget * 0.15
        )

        storage = round(
            budget * 0.15
        )

        buffer = (
            budget
            - furniture
            - lighting
            - decor
            - storage
        )

        allocations = [
            {
                "category": "Furniture",
                "amount": furniture,
                "reason": "Core functional pieces",
            },
            {
                "category": "Lighting",
                "amount": lighting,
                "reason": "Layered practical lighting",
            },
            {
                "category": "Decor",
                "amount": decor,
                "reason": "Accent and wall decor",
            },
            {
                "category": "Storage",
                "amount": storage,
                "reason": "Keep rooms organized",
            },
            {
                "category": "Buffer",
                "amount": buffer,
                "reason": "Price variation and extras",
            },
        ]

        rooms = ", ".join(
            data.get(
                "rooms",
                [],
            )
        )

        summary = (
            f"A practical "
            f"{data.get('style', 'modern')} "
            f"home setup for {rooms}, "
            f"keeping the total plan near "
            f"₹{budget:,}."
        )

        tips = [
            "Measure rooms before buying furniture.",
            "Prioritize frequently used items first.",
            "Keep a small buffer for delivery and installation.",
        ]

    elif planner == "party":

        food = round(
            budget * 0.45
        )

        venue = round(
            budget * 0.20
        )

        decoration = round(
            budget * 0.15
        )

        entertainment = round(
            budget * 0.10
        )

        buffer = (
            budget
            - food
            - venue
            - decoration
            - entertainment
        )

        allocations = [
            {
                "category": "Food & Catering",
                "amount": food,
                "reason": "Guest-focused spend",
            },
            {
                "category": "Venue",
                "amount": venue,
                "reason": "Space and basic facilities",
            },
            {
                "category": "Decoration",
                "amount": decoration,
                "reason": "Theme and atmosphere",
            },
            {
                "category": "Entertainment",
                "amount": entertainment,
                "reason": "Activities and music",
            },
            {
                "category": "Buffer",
                "amount": buffer,
                "reason": "Unexpected event costs",
            },
        ]

        guests = max(
            int(data.get("guests", 1)),
            1,
        )

        per_guest = budget / guests

        summary = (
            f"A {data.get('event_type', 'party')} "
            f"plan for {guests} guests with an "
            f"estimated ₹{per_guest:,.0f} per guest."
        )

        tips = [
            "Confirm the final guest count before ordering food.",
            "Compare venue inclusions before booking.",
            "Reserve contingency money for last-minute changes.",
        ]

    else:

        earrings = round(
            budget * 0.25
        )

        necklace = round(
            budget * 0.40
        )

        other = round(
            budget * 0.20
        )

        buffer = (
            budget
            - earrings
            - necklace
            - other
        )

        allocations = [
            {
                "category": "Earrings",
                "amount": earrings,
                "reason": "Easy occasion accent",
            },
            {
                "category": "Necklace",
                "amount": necklace,
                "reason": "Main statement piece",
            },
            {
                "category": "Bracelet/Ring",
                "amount": other,
                "reason": "Balanced accessories",
            },
            {
                "category": "Buffer",
                "amount": buffer,
                "reason": "Alternative styles or price variation",
            },
        ]

        image_note = ""

        if image_supplied:
            image_note = (
                " The uploaded outfit image was received "
                "and can be used as an additional visual cue."
            )

        summary = (
            f"An {data.get('style', 'elegant')} "
            f"jewelry direction for a "
            f"{data.get('occasion', 'special')} "
            f"occasion within ₹{budget:,}."
            f"{image_note}"
        )

        tips = [
            "Choose one statement piece and keep other pieces simpler.",
            "Match metal tone with the outfit and occasion.",
            "Check dimensions and material details before purchasing.",
        ]

    return {
        "summary": summary,
        "allocations": allocations,
        "recommendations": items,
        "tips": tips,
    }


def _prompt(
    planner: str,
    data: dict,
) -> str:

    catalog = catalog_for(
        planner,
        int(data["budget"]),
    )

    return f"""
You are PocketSmart AI,
a budget recommendation assistant.

Planner:
{planner}

User input:
{json.dumps(data, ensure_ascii=False)}

Demo catalog:
{json.dumps(catalog, ensure_ascii=False)}

Create a practical budget-aware plan.

Important:
- The catalog is simulated.
- Do not claim live availability.
- Do not invent product URLs.
- Respect the user's total budget.
- Use only catalog items for recommendations.

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
  "summary": "string",
  "allocations": [
    {{
      "category": "string",
      "amount": number,
      "reason": "string"
    }}
  ],
  "recommendations": [
    {{
      "title": "string",
      "platform": "string",
      "category": "string",
      "price": number,
      "rating": number,
      "url": "string"
    }}
  ],
  "tips": [
    "string"
  ]
}}

Return between 3 and 6 recommendations.
"""


def _extract_json(text: str) -> dict:

    text = text.strip()

    if text.startswith("```"):
        text = text.replace(
            "```json",
            "",
            1,
        )

        if text.endswith("```"):
            text = text[:-3]

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "Gemini response did not contain JSON"
        )

    return json.loads(
        text[start:end + 1]
    )


def generate_recommendation(
    planner: str,
    data: dict,
    image_bytes: bytes | None = None,
    mime_type: str | None = None,
):

    if (
        not settings.gemini_api_key
        or genai is None
    ):
        return (
            _fallback(
                planner,
                data,
                bool(image_bytes),
            ),
            "fallback",
        )

    try:

        client = genai.Client(
            api_key=settings.gemini_api_key
        )

        prompt = _prompt(
            planner,
            data,
        )

        contents: list[Any] = [
            prompt
        ]

        if (
            image_bytes
            and mime_type
            and types
        ):

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                )
            )

        config = None

        if types:
            config = types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=3000,
            )

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=config,
        )

        raw = response.text or ""

        parsed = _extract_json(raw)

        if not isinstance(
            parsed.get("recommendations"),
            list,
        ):
            raise ValueError(
                "Invalid recommendation structure"
            )

        if not isinstance(
            parsed.get("allocations"),
            list,
        ):
            raise ValueError(
                "Invalid allocation structure"
            )

        if not isinstance(
            parsed.get("tips"),
            list,
        ):
            raise ValueError(
                "Invalid tips structure"
            )

        known_catalog = catalog_for(
            planner,
            int(data["budget"]),
        )

        known_urls = {
            item["url"]
            for item in known_catalog
        }

        cleaned_recommendations = []

        for item in parsed["recommendations"]:

            if not isinstance(item, dict):
                continue

            if item.get("url") not in known_urls:
                continue

            cleaned_recommendations.append(
                {
                    "title": str(
                        item.get(
                            "title",
                            "Recommendation",
                        )
                    ),
                    "platform": str(
                        item.get(
                            "platform",
                            "Platform",
                        )
                    ),
                    "category": str(
                        item.get(
                            "category",
                            "General",
                        )
                    ),
                    "price": int(
                        item.get(
                            "price",
                            0,
                        )
                    ),
                    "rating": float(
                        item.get(
                            "rating",
                            0,
                        )
                    ),
                    "url": item["url"],
                }
            )

        if not cleaned_recommendations:
            raise ValueError(
                "Gemini returned no valid catalog recommendations"
            )

        parsed["recommendations"] = (
            cleaned_recommendations[:6]
        )

        return parsed, "gemini"

    except Exception as exc:

        logger.warning(
            "Gemini request failed; using fallback: %s",
            exc,
        )

        return (
            _fallback(
                planner,
                data,
                bool(image_bytes),
            ),
            "fallback",
        )