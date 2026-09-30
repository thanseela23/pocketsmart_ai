"""
Local demo catalog.

These are simulated recommendations for the project demo.
They are NOT live inventory or live prices.
"""


CATALOG = {

    "home": [

        {
            "title": "Minimal LED Ceiling Light",
            "platform": "IKEA",
            "category": "lighting",
            "price": 2499,
            "rating": 4.5,
            "url": "https://www.ikea.com/",
        },

        {
            "title": "Modern 1200mm Ceiling Fan",
            "platform": "Amazon",
            "category": "fan",
            "price": 3299,
            "rating": 4.3,
            "url": "https://www.amazon.in/",
        },

        {
            "title": "Compact 4-Seater Dining Table",
            "platform": "Flipkart",
            "category": "dining",
            "price": 8999,
            "rating": 4.2,
            "url": "https://www.flipkart.com/",
        },

        {
            "title": "Scandinavian Accent Chair",
            "platform": "IKEA",
            "category": "furniture",
            "price": 6999,
            "rating": 4.4,
            "url": "https://www.ikea.com/",
        },

        {
            "title": "Neutral Wall Art Set",
            "platform": "Amazon",
            "category": "decor",
            "price": 1599,
            "rating": 4.1,
            "url": "https://www.amazon.in/",
        },

        {
            "title": "Warm Table Lamp",
            "platform": "Flipkart",
            "category": "lighting",
            "price": 1299,
            "rating": 4.0,
            "url": "https://www.flipkart.com/",
        },

        {
            "title": "Storage Cabinet",
            "platform": "IKEA",
            "category": "storage",
            "price": 5999,
            "rating": 4.3,
            "url": "https://www.ikea.com/",
        },
    ],

    "party": [

        {
            "title": "Family Catering Package",
            "platform": "Swiggy",
            "category": "catering",
            "price": 8500,
            "rating": 4.4,
            "url": "https://www.swiggy.com/",
        },

        {
            "title": "Party Catering Package",
            "platform": "Zomato",
            "category": "catering",
            "price": 10500,
            "rating": 4.3,
            "url": "https://www.zomato.com/",
        },

        {
            "title": "Budget Event Decoration",
            "platform": "Zomato",
            "category": "decoration",
            "price": 4500,
            "rating": 4.1,
            "url": "https://www.zomato.com/",
        },

        {
            "title": "Premium Event Decoration",
            "platform": "Swiggy",
            "category": "decoration",
            "price": 7500,
            "rating": 4.2,
            "url": "https://www.swiggy.com/",
        },

        {
            "title": "Local Event Hall Stay Package",
            "platform": "OYO",
            "category": "venue",
            "price": 9000,
            "rating": 4.0,
            "url": "https://www.oyorooms.com/",
        },

        {
            "title": "Entertainment Starter Package",
            "platform": "Local Vendor",
            "category": "entertainment",
            "price": 3500,
            "rating": 4.2,
            "url": "#",
        },
    ],

    "jewelry": [

        {
            "title": "Classic Gold-Tone Stud Earrings",
            "platform": "Amazon",
            "category": "earrings",
            "price": 1299,
            "rating": 4.3,
            "url": "https://www.amazon.in/",
        },

        {
            "title": "Pearl Drop Earrings",
            "platform": "Flipkart",
            "category": "earrings",
            "price": 1799,
            "rating": 4.4,
            "url": "https://www.flipkart.com/",
        },

        {
            "title": "Minimal Pendant Necklace",
            "platform": "Amazon",
            "category": "necklace",
            "price": 2499,
            "rating": 4.2,
            "url": "https://www.amazon.in/",
        },

        {
            "title": "Statement Necklace Set",
            "platform": "Flipkart",
            "category": "necklace",
            "price": 3999,
            "rating": 4.1,
            "url": "https://www.flipkart.com/",
        },

        {
            "title": "Elegant Bracelet",
            "platform": "Amazon",
            "category": "bracelet",
            "price": 1599,
            "rating": 4.0,
            "url": "https://www.amazon.in/",
        },

        {
            "title": "Occasion Ring",
            "platform": "Flipkart",
            "category": "ring",
            "price": 2199,
            "rating": 4.2,
            "url": "https://www.flipkart.com/",
        },
    ],
}


def catalog_for(
    planner: str,
    budget: int,
) -> list[dict]:

    items = [
        item.copy()
        for item in CATALOG.get(
            planner,
            [],
        )
    ]

    affordable = [
        item
        for item in items
        if item["price"] <= budget
    ]

    selected = affordable or items

    return sorted(
        selected,
        key=lambda item: (
            item["price"],
            -item["rating"],
        ),
    )[:6]
    