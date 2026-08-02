import re


def check_password(password):

    score = 0

    common_passwords = [
        "123456",
        "12345678",
        "password",
        "password123",
        "admin",
        "welcome",
        "qwerty",
        "abc123",
        "letmein"
    ]

    result = {
        "length": False,
        "uppercase": False,
        "lowercase": False,
        "number": False,
        "special": False,
        "score": 0,
        "strength": "Weak",
        "risk_score": 0,
        "entropy": 0,
        "suggestions": [],
        "crack_time": "-"
    }

    if len(password) >= 8:
        result["length"] = True
        score += 1

    if re.search(r"[A-Z]", password):
        result["uppercase"] = True
        score += 1

    if re.search(r"[a-z]", password):
        result["lowercase"] = True
        score += 1

    if re.search(r"[0-9]", password):
        result["number"] = True
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        result["special"] = True
        score += 1

    result["score"] = score

    result["risk_score"] = score * 20
    result["entropy"] = len(password) * score * 4

    if password.lower() in common_passwords:
        result["risk_score"] = max(0, result["risk_score"] - 40)
        result["suggestions"].append(
            "⚠ This is a very common password. Avoid using it."
        )

    if score <= 2:
        result["strength"] = "Weak"
    elif score <= 4:
        result["strength"] = "Medium"
    else:
        result["strength"] = "Strong"

    if score <= 2:
        result["crack_time"] = "Few Seconds"
    elif score == 3:
        result["crack_time"] = "Few Minutes"
    elif score == 4:
        result["crack_time"] = "Several Hours"
    else:
        result["crack_time"] = "Many Years"

    if not result["suggestions"]:
        result["suggestions"].append(
            "✅ No security issues detected."
        )

    return result