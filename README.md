# 🔐 SafePass-Checker

A smart Python **Password Strength Checker** that evaluates a password's strength using multiple metrics:
length, character variety, estimated entropy, repeated/sequential patterns, and common-password detection.  
Provides a clear **score**, **human-friendly feedback**, and **actionable suggestions**.

---

## Features
- Length and character class checks (lower, upper, digits, symbols)  
- Entropy estimate (bits) and strength rating (Very Weak → Very Strong)  
- Detects: repeated characters, keyboard sequences, ascending/descending numeric sequences  
- Detects common weak passwords (e.g., "password", "123456")  
- Provides suggestions to improve password strength

---

## How to run
```bash
python password_checker.py
