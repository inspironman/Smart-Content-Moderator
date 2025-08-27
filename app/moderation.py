from sightengine.client import SightengineClient
import os
import tempfile
from dotenv import load_dotenv
import requests

load_dotenv()

api_user = os.getenv("SIGHTENGINE_API_USER")
api_secret = os.getenv("SIGHTENGINE_API_SECRET")
client = SightengineClient(api_user, api_secret)

def moderate_text_sightengine(text: str, lang="en"):
    url = "https://api.sightengine.com/1.0/text/check.json"
    data = {
        "text": text,
        "lang": lang,
        "categories": "toxic, spam, harassment, safe, personal, link, extremism, violence, self-harm",
        "mode": "rules",
        "api_user": api_user,
        "api_secret": api_secret,
    }
    response = requests.post(url, data=data)
    result = response.json()

    flagged_categories = []
    # Skip 'status' and 'request' keys
    for category, details in result.items():
        if category in ("status", "request"):
            continue
        if "matches" in details and details["matches"]:
            flagged_categories.append(category)

    if flagged_categories:
        classification = ",".join(flagged_categories)
        confidence = 0.9  # heuristic confidence
        reasoning = f"Flagged categories detected: {classification}"
    else:
        classification = "safe"
        confidence = 0.99
        reasoning = "No inappropriate content detected"

    return {
        "classification": classification,
        "confidence": confidence,
        "reasoning": reasoning,
        "llm_response": str(result),
    }


def moderate_image_sightengine(image_bytes: bytes):
    with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
        tmp_file.write(image_bytes)
        tmp_file.flush()

        # Request all moderation models you want to check
        result = client.check("nudity", "violence", "weapon", "alcohol", "drugs").set_file(tmp_file.name)

    classification = "safe"
    confidence = 0.99
    reasoning = "No flagged content detected"

    # List of (model_key in result, value_key to check, threshold, classification, reasoning)
    checks = [
        ("nudity", "raw", 0.5, "inappropriate", "Nudity detected"),
        ("violence", "raw", 0.5, "inappropriate", "Violence detected"),
        ("weapon", "prob", 0.5, "inappropriate", "Weapons detected"),
        ("alcohol", "prob", 0.5, "inappropriate", "Alcohol detected"),
        ("drugs", "prob", 0.5, "inappropriate", "Drugs detected"),
    ]

    for model_key, value_key, threshold, class_label, reason in checks:
        if model_key in result and result[model_key].get(value_key, 0) > threshold:
            classification = class_label
            confidence = result[model_key][value_key]
            reasoning = reason
            break  # stop at first detected flagged content

    return {
        "classification": classification,
        "confidence": confidence,
        "reasoning": reasoning,
        "llm_response": str(result),
    }
