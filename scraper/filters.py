import re

# Detect cricket match related text
KEYWORDS = ["cricket", "odi", "t20", "test", "match", "league", "teams"]

def is_relevant(text):
    text = text.lower()
    return any(k in text for k in KEYWORDS)
