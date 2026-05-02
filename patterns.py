# =============================================================================
# patterns.py — Member 1
# All threat detection patterns, keywords, and their weights.
# Each pattern has a name, a regex rule, and a score weight (how dangerous it is).
# =============================================================================

import re

# ─────────────────────────────────────────────
# REGEX-BASED THREAT PATTERNS
# Each entry: (pattern_name, compiled_regex, weight, description)
# ─────────────────────────────────────────────

REGEX_PATTERNS = [

    # ── SQL Injection ──────────────────────────────────────────────────────
    (
        "SQL Injection — OR bypass",
        re.compile(r"('\s*(or|OR)\s*'?\d+\s*'?\s*=\s*'?\d+|'\s*(or|OR)\s+[\w]+\s*=\s*[\w]+)", re.IGNORECASE),
        40,
        "Classic OR-based SQL auth bypass detected (e.g., ' OR 1=1)"
    ),
    (
        "SQL Injection — UNION SELECT",
        re.compile(r"\bUNION\b.{0,20}\bSELECT\b", re.IGNORECASE),
        40,
        "UNION SELECT statement detected — likely data extraction attempt"
    ),
    (
        "SQL Injection — DROP / DELETE",
        re.compile(r"\b(DROP|DELETE|TRUNCATE)\s+(TABLE|DATABASE|FROM)\b", re.IGNORECASE),
        45,
        "Destructive SQL command detected (DROP/DELETE/TRUNCATE)"
    ),
    (
        "SQL Injection — comment termination",
        re.compile(r"(--|#|/\*)\s*$", re.MULTILINE),
        25,
        "SQL comment sequence detected — often used to terminate queries"
    ),
    (
        "SQL Injection — INSERT / UPDATE",
        re.compile(r"\b(INSERT\s+INTO|UPDATE\s+\w+\s+SET)\b", re.IGNORECASE),
        30,
        "SQL write operation detected (INSERT/UPDATE)"
    ),

    # ── Cross-Site Scripting (XSS) ─────────────────────────────────────────
    (
        "XSS — script tag",
        re.compile(r"<\s*script[\s>]", re.IGNORECASE),
        35,
        "HTML <script> tag detected — common XSS vector"
    ),
    (
        "XSS — javascript: protocol",
        re.compile(r"javascript\s*:", re.IGNORECASE),
        35,
        "javascript: protocol detected — used in href/src XSS attacks"
    ),
    (
        "XSS — event handler",
        re.compile(r"\bon\w+\s*=\s*[\"']?\s*(alert|eval|document|window)", re.IGNORECASE),
        30,
        "Inline event handler with JS execution detected (e.g., onerror=alert)"
    ),
    (
        "XSS — eval / document.cookie",
        re.compile(r"\b(eval\s*\(|document\.cookie|document\.write\s*\()", re.IGNORECASE),
        30,
        "Dangerous JS function detected (eval / document.cookie)"
    ),
    (
        "XSS — iframe injection",
        re.compile(r"<\s*iframe[\s>]", re.IGNORECASE),
        25,
        "iframe tag detected — can embed malicious pages"
    ),

    # ── Command Injection ──────────────────────────────────────────────────
    (
        "Command Injection — shell chaining",
        re.compile(r"(;\s*(rm|wget|curl|bash|sh|python|perl|nc|netcat)\b)", re.IGNORECASE),
        45,
        "Shell command chaining detected (e.g., ; rm -rf, ; wget)"
    ),
    (
        "Command Injection — pipe to shell",
        re.compile(r"\|\s*(bash|sh|cmd|powershell)", re.IGNORECASE),
        45,
        "Pipe to shell detected — likely command execution attempt"
    ),
    (
        "Command Injection — backtick execution",
        re.compile(r"`[^`]+`"),
        35,
        "Backtick command substitution detected"
    ),
    (
        "Command Injection — redirect operators",
        re.compile(r"(>>|>\s*/etc/|>\s*/dev/)"),
        30,
        "File redirect to sensitive path detected"
    ),
    (
        "Command Injection — path traversal",
        re.compile(r"(\.\./){2,}|(%2e%2e%2f){2,}", re.IGNORECASE),
        35,
        "Path traversal sequence detected (../../)"
    ),

    # ── Suspicious URL Paths ───────────────────────────────────────────────
    (
        "Suspicious URL — admin panel",
        re.compile(r"/(admin|administrator|wp-admin|cpanel|phpmyadmin)\b", re.IGNORECASE),
        20,
        "Admin panel URL path detected"
    ),
    (
        "Suspicious URL — login/auth",
        re.compile(r"/(login|signin|auth|authenticate|session)\b", re.IGNORECASE),
        15,
        "Authentication URL path detected"
    ),
    (
        "Suspicious URL — config/env files",
        re.compile(r"\.(env|config|cfg|ini|bak|backup|sql|db)\b", re.IGNORECASE),
        30,
        "Sensitive file extension detected in URL"
    ),
]


# ─────────────────────────────────────────────
# KEYWORD-BASED THREAT PATTERNS
# Flat list of suspicious keywords with weights
# ─────────────────────────────────────────────

KEYWORD_GROUPS = [
    {
        "name": "Phishing keywords",
        "weight": 15,
        "description": "Social engineering language detected",
        "keywords": [
            "urgent", "click now", "verify your account", "confirm your identity",
            "your account has been suspended", "limited time", "act immediately",
            "your password", "update your password", "reset password",
            "bank details", "credit card", "you have won", "claim your prize",
        ]
    },
    {
        "name": "Credential harvesting",
        "weight": 20,
        "description": "Keywords associated with credential theft",
        "keywords": [
            "enter your password", "submit your password", "provide your pin",
            "social security", "ssn", "date of birth", "mother's maiden name",
        ]
    },
    {
        "name": "Malware / exploit language",
        "weight": 25,
        "description": "Language associated with malware delivery or exploitation",
        "keywords": [
            "download and run", "execute payload", "disable antivirus",
            "bypass firewall", "exploit", "zero-day", "shellcode",
            "reverse shell", "bind shell", "meterpreter",
        ]
    },
]


# ─────────────────────────────────────────────
# RISK LEVEL THRESHOLDS
# ─────────────────────────────────────────────

RISK_LEVELS = [
    (0,  30,  "Safe",   "#27ae60"),   # green
    (30, 70,  "Medium", "#f39c12"),   # orange
    (70, 101, "High",   "#e74c3c"),   # red
]
