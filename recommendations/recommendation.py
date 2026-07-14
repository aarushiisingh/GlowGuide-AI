from recommendations.recommendation_database import DATABASE

def get_recommendations(tone, undertone):

    key = (tone, undertone)

    if key in DATABASE:
        return DATABASE[key]

    print(f"Recommendation not found for {key}. Using Fair Neutral.")

    return DATABASE[("Fair", "Neutral")]