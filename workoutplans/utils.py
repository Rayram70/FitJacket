import requests
import json
from django.conf import settings


def generate_workout_plan(user_input):
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Referer": "http://127.0.0.1:8000",  # Required by OpenRouter
        "X-Title": "FitJacket",  # Required by OpenRouter
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are an expert fitness trainer. Generate a detailed, personalized workout plan based on:

    USER REQUIREMENTS:
    {user_input}

    RESPONSE FORMAT:
    - Goal: [clear goal statement]
    - Duration: [program duration]
    - Weekly Schedule: [day-by-day breakdown]
    - Exercises: [detailed exercises with sets/reps]
    - Equipment Needed: [list]
    - Pro Tips: [expert advice]
    - Safety Notes: [important precautions]
    """

    payload = {
        "model": settings.DEEPSEEK_MODEL_ID,
        "messages": [
            {"role": "system",
             "content": "You are a professional fitness coach. Provide clear, safe, and effective workout plans."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1500  # Adjust based on your needs
    }

    try:
        response = requests.post(settings.OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Error: {str(e)}")
        return None