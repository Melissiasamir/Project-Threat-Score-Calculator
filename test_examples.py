# =============================================================================
# test_examples.py — Quick test runner (no pytest needed)
# Run with:  python test_examples.py
# =============================================================================

from analyzer import analyze_input

test_inputs = [
    "urgent click here <script>alert(1)</script>",
    "' OR 1=1 --",
    "/admin login page",
    "normal safe text"
]

for text in test_inputs:
    print("\nInput:", text)
    result = analyze_input(text)
    print("Output:", result)