import re
from skill_dictionary import SKILL_DICTIONARY


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text):
    return text.split()


def detect_skills(text):
    detected = []
    for category, skills in SKILL_DICTIONARY.items():
        for skill in skills:
            if skill in text:
                detected.append({
                    "skill": skill,
                    "category": category
                })
    return detected


def process_text(raw_text):
    cleaned = clean_text(raw_text)
    tokens = tokenize(cleaned)
    skills = detect_skills(cleaned)

    return {
        "raw_text": raw_text,
        "clean_text": cleaned,
        "tokens": tokens,
        "skills_detected": skills
    }