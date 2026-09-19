import math
import re
import sys

COMMON_PASSWORDS = {
    "123456",
    "password",
    "123456789",
    "12345678",
    "qwerty",
    "abc123",
    "football",
    "monkey",
    "letmein",
    "111111",
    "1234",
    "passw0rd",
    "iloveyou",
    "admin",
    "welcome"
}

KEYBOARD_SEQUENCES = [
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "12345",
    "67890"
]


def char_classes(password):
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_symbol = bool(re.search(r"[^A-Za-z0-9]", password))

    count = sum([
        has_lower,
        has_upper,
        has_digit,
        has_symbol
    ])

    return {
        "lower": has_lower,
        "upper": has_upper,
        "digit": has_digit,
        "symbol": has_symbol,
        "count": count
    }


def estimate_entropy(password):
    classes = char_classes(password)
    pool = 0

    if classes["lower"]:
        pool += 26
    if classes["upper"]:
        pool += 26
    if classes["digit"]:
        pool += 10
    if classes["symbol"]:
        pool += 32

    pool = max(pool, 1)
    return len(password) * math.log2(pool)


def detect_repeats(password):
    problems = []

    match = re.search(r"(.)\1{2,}", password)

    if match:
        problems.append(
            f"Repeated character: '{match.group(1)}' x{len(match.group(0))}"
        )

    for size in range(2, 6):
        if len(password) >= size * 2:
            piece = password[:size]

            if piece * (len(password) // size) == password:
                problems.append(f"Repeated pattern: '{piece}'")
                break

    return problems


def detect_sequences(password):
    problems = []

    numbers = re.findall(r"\d+", password)

    for number in numbers:
        if len(number) >= 3:
            ascending = all(
                int(number[i + 1]) - int(number[i]) == 1
                for i in range(len(number) - 1)
            )

            descending = all(
                int(number[i]) - int(number[i + 1]) == 1
                for i in range(len(number) - 1)
            )

            if ascending:
                problems.append(
                    f"Numeric ascending sequence: {number}"
                )

            if descending:
                problems.append(
                    f"Numeric descending sequence: {number}"
                )

    password_lower = password.lower()

    for sequence in KEYBOARD_SEQUENCES:
        if sequence in password_lower:
            problems.append(
                f"Keyboard sequence: '{sequence}'"
            )

    return problems


def score_password(password):
    problems = []
    suggestions = []

    length = len(password)
    classes = char_classes(password)

    if password.lower() in COMMON_PASSWORDS:
        problems.append("Common password detected")
        suggestions.append("Avoid commonly used passwords")

    if length < 6:
        problems.append("Very short password")
        suggestions.append("Use a longer password, preferably 12+ characters")
    elif length < 8:
        problems.append("Short password")
        suggestions.append("Aim for at least 8 characters")

    if classes["count"] < 2:
        problems.append("Low character variety")
        suggestions.append(
            "Use a mix of uppercase, lowercase, digits, and symbols"
        )

    repeats = detect_repeats(password)

    if repeats:
        problems.extend(repeats)
        suggestions.append(
            "Avoid repeated characters and simple repeated patterns"
        )

    sequences = detect_sequences(password)

    if sequences:
        problems.extend(sequences)
        suggestions.append(
            "Avoid sequential characters and keyboard patterns"
        )

    entropy = estimate_entropy(password)

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

    penalty = 0

    if length < 8:
        penalty += 10

    if classes["count"] == 1:
        penalty += 20

    if password.lower() in COMMON_PASSWORDS:
        penalty += 30

    if repeats:
        penalty += 10

    if sequences:
        penalty += 10

    score = max(
        0,
        min(100, base_score - penalty + int((entropy / 100) * 20))
    )

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

    if rating in ("Very Weak", "Weak"):
        suggestions.append("Increase the password length to 12+ characters")

    if classes["count"] < 3:
        suggestions.append(
            "Use at least three different character types"
        )

    return {
        "score": score,
        "rating": rating,
        "entropy_bits": round(entropy, 1),
        "problems": problems,
        "suggestions": suggestions
    }


def interactive_prompt():
    print("=" * 60)
    print("SafePass-Checker")
    print("Enter a password to evaluate. Type 'q' to quit.")
    print("=" * 60)

    while True:
        password = input("\nPassword: ")

        if password.lower() == "q":
            print("Goodbye!")
            break

        result = score_password(password)

        print(
            f"\nScore: {result['score']} / 100"
            f"  Rating: {result['rating']}"
        )
        print(f"Estimated entropy: {result['entropy_bits']} bits")

        if result["problems"]:
            print("\nProblems:")

            for problem in result["problems"]:
                print(" -", problem)

        if result["suggestions"]:
            print("\nSuggestions:")

            for suggestion in result["suggestions"]:
                print(" -", suggestion)

        print(
            "\nThis is an educational estimate. "
            "Do not enter passwords you actually use."
        )


def run_demo_tests():
    examples = [
        "password",
        "12345678",
        "hunter2",
        "P@ssw0rd!",
        "correcthorsebatterystaple",
        "Tr0ub4dor&3",
        "Aa1!",
        "LongerAnd$tronger123"
    ]

    for password in examples:
        result = score_password(password)

        print(f"\nPassword: {password}")
        print(
            f"Score: {result['score']}  "
            f"Rating: {result['rating']}  "
            f"Entropy: {result['entropy_bits']} bits"
        )

        if result["problems"]:
            print("Problems:", "; ".join(result["problems"]))

        if result["suggestions"]:
            print("Suggestions:", "; ".join(result["suggestions"]))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo_tests()
    else:
        interactive_prompt()
