# =============================================================================
# analyzer.py — Member 2 (Part B)
# Core analysis engine.
# Runs the preprocessed input through all regex and keyword patterns
# and returns a list of matched threats with their weights and descriptions.
# =============================================================================



from patterns import REGEX_PATTERNS, KEYWORD_GROUPS
from utils import clean_text


def analyze_input(user_input: str):
    """
    Analyze input and return detected threats
    """

    # Step 1: Clean input
    cleaned = clean_text(user_input)

    detected_threats = []

    # ─────────────────────────────────────────
    # Step 2: Regex Detection
    # ─────────────────────────────────────────
    for name, pattern, weight, description in REGEX_PATTERNS:
        match = pattern.search(cleaned)

        if match:
            detected_threats.append({
                "type": "regex",
                "name": name,
                "weight": weight,
                "description": description,
                "matched_text": match.group()  # 🔥 BONUS
            })

    # ─────────────────────────────────────────
    # Step 3: Keyword Detection
    # ─────────────────────────────────────────
    for group in KEYWORD_GROUPS:
        for keyword in group["keywords"]:
            if keyword in cleaned:
                detected_threats.append({
                    "type": "keyword",
                    "name": group["name"],
                    "weight": group["weight"],
                    "description": group["description"],
                    "matched_text": keyword  # 🔥 BONUS
                })
                break  # prevent duplicates

    return detected_threats



if __name__ == "__main__":
    text = "urgent click here <script>alert(1)</script> /admin"
    result = analyze_input(text)
    print(result)