# =============================================================================
# utils.py — Member 2 (Part A)
# Text preprocessing utilities.
# Cleans and normalizes input before analysis so patterns match reliably.
# =============================================================================


import re

def clean_text(text: str) -> str:
    """
    Normalize input text for better pattern matching
    """

    # Convert to lowercase
    text = text.lower()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text