def get_recommendations(tone, undertone):

    database = {

        ("Fair", "Cool"): {
            "Foundation": "Ivory",
            "Lipstick": "Rose Pink",
            "Blush": "Soft Pink",
            "Eyeshadow": "Silver"
        },

        ("Fair", "Warm"): {
            "Foundation": "Warm Ivory",
            "Lipstick": "Coral",
            "Blush": "Peach",
            "Eyeshadow": "Gold"
        },

        ("Medium", "Warm"): {
            "Foundation": "Golden Beige",
            "Lipstick": "Terracotta",
            "Blush": "Peach",
            "Eyeshadow": "Bronze"
        },

        ("Medium", "Neutral"): {
            "Foundation": "Natural Beige",
            "Lipstick": "Nude Pink",
            "Blush": "Rose",
            "Eyeshadow": "Taupe"
        },

        ("Tan", "Warm"): {
            "Foundation": "Honey",
            "Lipstick": "Brick Red",
            "Blush": "Burnt Peach",
            "Eyeshadow": "Copper"
        },

        ("Deep", "Cool"): {
            "Foundation": "Espresso",
            "Lipstick": "Berry",
            "Blush": "Plum",
            "Eyeshadow": "Purple"
        }

    }

    return database.get(
        (tone, undertone),
        {
            "Foundation": "Natural",
            "Lipstick": "Nude",
            "Blush": "Peach",
            "Eyeshadow": "Brown"
        }
    )