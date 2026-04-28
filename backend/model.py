from transformers import pipeline
from langdetect import detect
import re

# Multilingual model (supports 100+ languages)
classifier = pipeline(
    "text-classification",
    model="papluca/xlm-roberta-base-language-detection"
)

fake_detector = pipeline(
    "text-classification",
    model="mrm8488/bert-tiny-finetuned-fake-news-detection"
)


def detect_location(text):
    cities = ["Hyderabad", "Mumbai", "Delhi", "Chennai", "Bangalore"]
    for city in cities:
        if city.lower() in text.lower():
            return city
    return None


def calculate_panic_index(text):
    panic_words = ["dead", "massive", "urgent", "immediately", "explosion", "flood"]
    count = 0
    for word in panic_words:
        count += text.lower().count(word)
    return min(count * 10, 100)


def analyze_text(text):

    # Language detection
    try:
        language = detect(text)
    except:
        language = "unknown"

    # Fake detection (English-focused)
    fake_result = fake_detector(text)[0]
    score = int(fake_result["score"] * 100)

    # Panic detection
    panic_index = calculate_panic_index(text)

    # Location extraction
    location = detect_location(text)

    # Tier logic
    if score > 80:
        status = "Auto Verified"
        action = "No Action"
    elif score > 60:
        status = "Suspicious"
        action = "Soft Label"
    elif score > 40:
        status = "Needs Review"
        action = "Human Review"
    else:
        status = "Likely Fake"
        action = "Auto-Flagged"

    return {
        "credibility_score": score,
        "status": status,
        "response_action": action,
        "location": location,
        "panic_index": panic_index,
        "language_detected": language
    }