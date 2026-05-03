import re
import html
import urllib.parse
import base64

# ----------------------------
# WEIGHTS (balanced for SOC behavior)
# ----------------------------
SQL_WEIGHT = 45
XSS_WEIGHT = 50
CMD_WEIGHT = 60
ENCODED_WEIGHT = 30
KEYWORD_WEIGHT = 10

# ----------------------------
# PATTERNS
# ----------------------------

SQL_PATTERNS = [
    r"(?i)(\bselect\b.*\bfrom\b)",
    r"(?i)(\bdrop\b\s+\btable\b)",
    r"(?i)(--|#)",
    r"(?i)\bor\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?",
    r"(?i)\band\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?",
]

XSS_PATTERNS = [
    r"(?i)<script.*?>.*?</script>",
    r"(?i)alert\s*\(",
    r"(?i)document\.cookie",
    r"(?i)onerror\s*=",
]

CMD_PATTERNS = [
    r"(?i);\s*rm\s+-rf",
    r"(?i)\|\s*whoami",
    r"(?i)&&",
]

KEYWORDS = ["password", "admin", "root", "token", "hack", "bypass"]


# ----------------------------
# INPUT NORMALIZATION
# ----------------------------

def decode_input(text: str) -> str:
    text = urllib.parse.unquote(text)
    text = html.unescape(text)

    try:
        decoded = base64.b64decode(text).decode("utf-8", errors="ignore")
        if decoded and decoded != text:
            text = text + " " + decoded
    except:
        pass

    return text.lower().strip()


def normalize(text: str) -> str:
    text = decode_input(text)
    text = re.sub(r"\s+", " ", text)
    return text


# ----------------------------
# MAIN SCORING ENGINE
# ----------------------------

def calculate_threat_score(user_input: str):

    text = normalize(user_input)

    score = 0
    reasons = []
    confidence = 100

    def add(points, msg):
        nonlocal score
        score += points
        reasons.append(msg)

    # ---------------- SQL Injection ----------------
    for p in SQL_PATTERNS:
        if re.search(p, text):
            add(SQL_WEIGHT, "SQL Injection detected")

    # ---------------- XSS ----------------
    for p in XSS_PATTERNS:
        if re.search(p, text):
            add(XSS_WEIGHT, "Cross-Site Scripting (XSS) detected")

    # ---------------- Command Injection ----------------
    for p in CMD_PATTERNS:
        if re.search(p, text):
            add(CMD_WEIGHT, "Command Injection detected")

    # ---------------- Keywords ----------------
    for w in KEYWORDS:
        if w in text:
            score += KEYWORD_WEIGHT
            reasons.append(f"Suspicious keyword: {w}")

    # ---------------- Encoded payload ----------------
    encoded = re.findall(r"%[0-9a-f]{2}", text)
    if len(encoded) > 3:
        score += ENCODED_WEIGHT
        reasons.append("Encoded payload detected")

    # ---------------- ESCALATION (IMPORTANT FIX) ----------------
    attack_count = len(reasons)

    if attack_count == 1:
        score += 10

    elif attack_count == 2:
        score += 25

    elif attack_count >= 3:
        score += 40
        reasons.append("MULTI-VECTOR ATTACK DETECTED")

    # ---------------- CRITICAL OVERRIDE (FIX HIGH RISK ISSUE) ----------------
    if re.search(r"(?i)<script>|alert\(|or\s+['\"]?1['\"]?\s*=\s*['\"]?1", text):
        score = max(score, 80)

    if re.search(r"(?i);|\|\s*rm|-rf|drop\s+table", text):
        score = max(score, 85)

    # ---------------- FINAL CAP ----------------
    score = min(score, 100)

    # ---------------- CONFIDENCE ----------------
    if attack_count == 0:
        confidence = 100
    else:
        confidence -= attack_count * 6

    confidence = max(0, min(confidence, 100))

    # ---------------- RISK LEVEL ----------------
    if score <= 30:
        level = "Safe"
    elif score <= 70:
        level = "Medium Risk"
    else:
        level = "High Risk"

    return score, level, reasons, confidence