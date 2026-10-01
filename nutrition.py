"""Nutrition-specific helpers (optional): offline fallback tips if Gemini Flash is unavailable."""

_FALLBACK_TIPS = {
    "weight": "Fill half your plate with vegetables and prioritise lean protein at every meal - it keeps you full longer and helps you eat fewer calories without feeling deprived.",
    "fat": "Fill half your plate with vegetables and prioritise lean protein at every meal - it keeps you full longer and helps you eat fewer calories without feeling deprived.",
    "muscle": "Include 20-40 g of protein in your post-workout meal (chicken, eggs, Greek yogurt or beans) and pair it with carbs to help your muscles recover and grow.",
    "gain": "Include 20-40 g of protein in your post-workout meal (chicken, eggs, Greek yogurt or beans) and pair it with carbs to help your muscles recover and grow.",
    "flex": "Stay well hydrated and get enough sleep - muscles and connective tissue recover and stay supple when you are rested and hydrated. Gentle stretching before bed helps too.",
}
_DEFAULT_TIP = "Drink water throughout the day, eat protein with every meal, and get 7-9 hours of sleep - recovery is where progress happens."


def fallback_tip(goal: str) -> str:
    g = (goal or "").lower()
    for keyword, tip in _FALLBACK_TIPS.items():
        if keyword in g:
            return tip
    return _DEFAULT_TIP
