# SafePass-Checker

SafePass-Checker is a Python command-line program that estimates password strength using several simple checks.

It considers password length, character variety, estimated entropy, repeated patterns, keyboard sequences, numeric sequences, and common passwords.

The project is intended for learning about password security concepts and basic Python programming.

## Features

- Checks password length
- Checks uppercase, lowercase, digits, and symbols
- Estimates password entropy in bits
- Detects common weak passwords
- Detects repeated characters and patterns
- Detects ascending and descending numeric sequences
- Detects simple keyboard sequences
- Gives a score from 0 to 100
- Provides a strength rating
- Gives suggestions for improvement
- Includes a demo mode with sample passwords

## Strength Ratings

| Score | Rating |
|---|---|
| 0–19 | Very Weak |
| 20–39 | Weak |
| 40–59 | Moderate |
| 60–79 | Strong |
| 80–100 | Very Strong |

The score is an estimate based on the checks implemented in the program. It is not a guarantee that a password is secure.

## How It Works

The program performs several checks on the password:

1. Checks whether the password is commonly used.
2. Checks its length.
3. Checks which character types are present.
4. Looks for repeated characters and simple repeated patterns.
5. Looks for numeric and keyboard sequences.
6. Estimates entropy based on the detected character types.
7. Combines these results into a score.
8. Displays problems and suggestions.

## Entropy Estimate

The program uses a simplified entropy calculation based on the possible character pool.

It estimates the pool using:

- 26 lowercase letters
- 26 uppercase letters
- 10 digits
- approximately 32 symbols

The estimated entropy is then calculated from the password length and detected character pool.

This is a simplified educational calculation and does not replace professional password-strength tools.

## Example

```text
============================================================
SafePass-Checker
Enter a password to evaluate. Type 'q' to quit.
============================================================

Password: password

Score: 0 / 100  Rating: Very Weak
Estimated entropy: 37.6 bits

Problems:
 - Common password detected
 - Short password

Suggestions:
 - Avoid commonly used passwords
 - Aim for at least 8 characters
 - Increase the password length to 12+ characters
 - Use at least three different character types
