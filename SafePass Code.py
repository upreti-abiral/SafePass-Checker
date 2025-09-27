```python
"""
SafePass-Checker
A professional-ish password strength evaluator.
"""

import math
import re
import sys

# Small list of extremely common weak passwords for quick detection.
COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "qwerty", "abc123", "football",
    "monkey", "letmein", "111111", "1234", "passw0rd", "iloveyou", "admin", "welcome"
}

KEYBOARD_SEQS = [
    "qwerty", "asdfgh", "zxcvbn", "12345", "67890"
]

def char_classes(password: str):
    """Return flags for presence of classes and count distinct classes."""
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_symbol = bool(re.search(r"[^A-Za-z0-9]", password))
    classes = sum([has_lower, has_upper, has_digit, has_symbol])
    return {"lower": has_lower, "upper": has_upper, "digit": has_digit, "symbol": has_symbol, "count": classes}

def estimate_entropy(password: str):
    """
    Rough entropy estimator:
    - For each char class present, assume pool size:
      lower=26, upper=26, digits=10, symbols=32 (approx)
    - Pool = sum of pools for detected classes
    - Entropy bits = len(password) * log2(pool)
    This is a simple conservative estimator (not zxcvbn-level).
    """
    classes = char_classes(password)
    pool = 0
    if classes["lower"]:
        pool += 26
    if classes["upper"]:
        pool += 26
    if classes["digit"]:
        pool += 10
    if classes["symbol"]:
        pool += 32  # approximate printable symbols
    pool = max(pool, 1)
    entropy = len(password) * math.log2(pool)
    return entropy

def detect_repeats(password: str):
    """Detect repeated characters or short repeated substrings."""
    repeats = []
    # repeated same char 3+ times
    m = re.search(r"(.)\1{2,}", password)
    if m:
        repeats.append(f"Repeated character: '{m.group(1)}' x{len(m.group(0))}")
    # repeated substrings like 'abab' or '1212'
    for size in range(2, 6):
        if len(password) >= size*2:
            piece = password[:size]
            if piece * (len(password)//size) == password:
                repeats.append(f"Repeated pattern: '{piece}'")
                break
    return repeats

def detect_sequences(password: str):
    """Detect simple ascending/descending numeric sequences or keyboard sequences."""
    problems = []
    # numeric ascending or descending sequences of length >= 3
    nums = re.findall(r"\d+", password)
    for n in nums:
        if len(n) >= 3:
            # check ascending
            asc = all(int(n[i+1]) - int(n[i]) == 1 for i in range(len(n)-1))
            desc = all(int(n[i]) - int(n[i+1]) == 1 for i in range(len(n)-1))
            if asc:
                problems.append(f"Numeric ascending sequence: {n}")
            if desc:
                problems.append(f"Numeric descending sequence: {n}")

    # keyboard-like sequences
    pl = password.lower()
    for seq in KEYBOARD_SEQS:
        if seq in pl:
            problems.append(f"Keyboard sequence: '{seq}'")
    return problems

def score_password(password: str):
    """Return a score 0-100 and a list of problems and suggestions."""
    problems = []
    suggestions = []
    length = len(password)

    # common password check
    if password.lower() in COMMON_PASSWORDS:
        problems.append("Common password detected")
        suggestions.append("Avoid using commonly known passwords")

    # length scoring
    if length < 6:
        problems.append("Very short password")
        suggestions.append("Make it longer (12+ recommended)")
    elif length < 8:
        problems.append("Short password")
        suggestions.append("Aim for 8+ characters; 12+ is better")

    # classes
    classes = char_classes(password)
    if classes["count"] < 2:
        problems.append("Low character variety (use upper, lower, digits, symbols)")
        suggestions.append("Mix uppercase, lowercase, digits, and symbols")

    # repeats and sequences
    repeats = detect_repeats(password)
    if repeats:
        problems.extend(repeats)
        suggestions.append("Avoid repeated characters or simple repeated patterns")

    seqs = detect_sequences(password)
    if seqs:
        problems.extend(seqs)
        suggestions.append("Avoid sequential characters or keyboard sequences")

    # entropy estimation
    entropy = estimate_entropy(password)
    # Map entropy to a score roughly:
    # 0-28 bits -> very weak, 28-40 -> weak, 40-60 -> moderate, 60-80 -> strong, 80+ -> very strong
    if entropy < 28:
        base_score = 10
    elif entropy < 40:
        base_score = 30
    elif entropy < 60:
        base_score = 55
    elif entropy < 80:
        base_score = 75
    else:
        base_score = 90

    # adjust score with penalties
    penalty = 0
    if length < 8:
        penalty += 10
    if classes["count"] == 1:
        penalty += 20
    if password.lower() in COMMON_PASSWORDS:
        penalty += 30
    if repeats:
        penalty += 10
    if seqs:
        penalty += 10

    score = max(0, min(100, base_score - penalty + int((entropy/100)*20)))  # small boost from entropy

    # Construct human-friendly rating
    if score < 20:
        rating = "Very Weak"
    elif score < 40:
        rating = "Weak"
    elif score < 60:
        rating = "Moderate"
    elif score < 80:
        rating = "Strong"
    else:
        rating = "Very Strong"

    # more tailored suggestions if not strong
    if rating in ("Very Weak", "Weak"):
        if "Make it longer (12+ recommended)" not in suggestions:
            suggestions.append("Increase length to 12+ characters")
    if classes["count"] < 3:
        suggestions.append("Use at least 3 types: uppercase, lowercase, digits, symbols")
    if "Avoid using commonly known passwords" not in suggestions and password.lower() in COMMON_PASSWORDS:
        suggestions.append("Do not use common passwords")

    return {
        "score": score,
        "rating": rating,
        "entropy_bits": round(entropy, 1),
        "problems": problems,
        "suggestions": suggestions
    }

def interactive_prompt():
    print("="*60)
    print("🔐 SafePass-Checker")
    print("Enter a password to evaluate. Type 'q' to quit.")
    print("="*60)
    while True:
        pwd = input("\nPassword: ")
        if pwd.lower() == 'q':
            print("Bye 👋")
            break
        result = score_password(pwd)
        print("\nScore: {score} / 100 — {rating}".format(score=result["score"], rating=result["rating"]))
        print(f"Estimated entropy: {result['entropy_bits']} bits")
        if result["problems"]:
            print("\nProblems:")
            for p in result["problems"]:
                print(" -", p)
        if result["suggestions"]:
            print("\nSuggestions:")
            for s in result["suggestions"]:
                print(" -", s)
        print("\n(Keep your real passwords private if you're concerned — this tool is for education.)")

# Small test runner you can run to see sample evaluations
def run_demo_tests():
    examples = [
        "password", "12345678", "hunter2", "P@ssw0rd!",
        "correcthorsebatterystaple", "Tr0ub4dor&3", "Aa1!", "LongerAnd$tronger123"
    ]
    for ex in examples:
        r = score_password(ex)
        print(f"\nPassword: {ex}")
        print(f" Score: {r['score']}  Rating: {r['rating']}, Entropy: {r['entropy_bits']} bits")
        if r['problems']:
            print(" Problems:", "; ".join(r['problems']))
        if r['suggestions']:
            print(" Suggestions:", "; ".join(r['suggestions']))

if __name__ == "__main__":
    # If user passes --demo, run tests instead of interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo_tests()
    else:
        interactive_prompt()
