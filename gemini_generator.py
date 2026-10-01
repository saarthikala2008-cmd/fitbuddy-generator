"""Gemini Pro: generates the structured 7-day workout plan."""
from app.config import GEMINI_PRO_MODEL
from app.gemini_client import generate_text


def generate_workout_gemini(user_input: dict) -> str:
    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for {user_input['name']}, aged {user_input['age']}, weighing {user_input['weight']} kg,
with the goal of **{user_input['goal']}**, who prefers **{user_input['intensity']} intensity** workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Include rest or active-recovery days where appropriate for the stated intensity.

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
"""
    return generate_text(GEMINI_PRO_MODEL, prompt)
