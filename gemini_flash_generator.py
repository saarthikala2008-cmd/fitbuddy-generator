"""Gemini Flash: generates a short nutrition / recovery tip."""
from app.config import GEMINI_FLASH_MODEL
from app.gemini_client import generate_text


def generate_nutrition_tip_with_flash(goal: str, age: int | None = None) -> str:
    """
    Generate a nutrition or recovery tip using Gemini Flash based on the user's fitness goal.

    Args:
        goal: The user's fitness goal, e.g. "weight loss", "muscle gain", "flexibility".
        age: Optional age, so the tip is appropriate for the person.
    Returns:
        The generated tip.
    """
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand. "
    )
    if age is not None:
        prompt += f"The person is {age} years old. "
        if age < 18:
            prompt += (
                "Because they are under 18, keep the tip safe and age-appropriate: suggest whole foods, "
                "water, sleep and play. Do NOT mention supplements, protein shakes, calorie counting, "
                "dieting or specific gram targets. "
            )
    prompt += "Keep it to 2-3 sentences, plain text, no markdown."
    return generate_text(GEMINI_FLASH_MODEL, prompt)