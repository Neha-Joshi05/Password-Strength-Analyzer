"""
education.py
Password security education content.
"""

EDUCATION = {
    "why_length": {
        "title": "Why Length > Complexity",
        "icon":  "📏",
        "content": """
**Length is the most powerful factor in password security.**

A 20-character password using only lowercase letters
has MORE entropy than an 8-character password with
uppercase, numbers and symbols.

| Password | Length | Entropy |
|----------|--------|---------|
| abc123!  | 7      | ~41 bits|
| correct-horse-battery-staple | 28 | ~184 bits |

Each extra character **multiplies** crack time.
Going from 8 → 12 chars = millions times harder!
""",
    },
    "entropy": {
        "title": "What is Entropy?",
        "icon":  "🎲",
        "content": """
**Entropy measures password unpredictability in bits.**

Formula: `H = L × log₂(R)`
- H = Entropy (bits)
- L = Password Length
- R = Character Pool Size

**Example:**
- 8 chars, lowercase only: 8 × log₂(26) = ~37 bits
- 8 chars, all types: 8 × log₂(94) = ~52 bits
- 16 chars, all types: 16 × log₂(94) = ~105 bits

Higher bits = exponentially harder to crack!
""",
    },
    "common_attacks": {
        "title": "Common Attack Methods",
        "icon":  "⚔️",
        "content": """
**How attackers crack passwords:**

🔴 **Dictionary Attack** — Try millions of known words/passwords
🔴 **Brute Force** — Try every combination (a, b...aa, ab...)
🔴 **Rainbow Tables** — Pre-computed hash lookups
🔴 **Credential Stuffing** — Use leaked username+password pairs
🔴 **Hybrid Attack** — Dictionary + rules (add 1, capitalize)
🔴 **Keyboard Walk** — Try qwerty, asdf patterns
🔴 **Personal Info** — Try name, birthday, city combos

**Modern GPU can try 10 BILLION passwords/second!**
""",
    },
    "passphrase": {
        "title": "Passphrase Power",
        "icon":  "💬",
        "content": """
**A passphrase = 4+ random unrelated words.**

Example: `Coffee-Brick-Dance-Moon`

**Why it works:**
✅ Long (20+ chars naturally)
✅ Easy to remember
✅ High entropy
✅ Resistant to dictionary attacks
✅ Follows NIST SP 800-63B guidelines

**Bad passphrase:** `ilovemycat` (predictable)
**Good passphrase:** `Thunder-Pixel-Mango-Volt`

The words must be RANDOM, not related to each other!
""",
    },
    "nist_guidelines": {
        "title": "NIST Password Guidelines",
        "icon":  "📋",
        "content": """
**NIST SP 800-63B (Latest Guidelines):**

✅ Minimum **8 characters** (recommend 16+)
✅ Check against **breached password lists**
✅ Allow **all printable ASCII** and spaces
✅ No mandatory **complexity rules**
✅ No mandatory **periodic resets**
✅ Support **password managers**
✅ Offer **multi-factor authentication**

❌ **Old (bad) advice:** Change every 90 days
✅ **New (good) advice:** Change only if compromised

NIST now says **length + randomness > complexity rules!**
""",
    },
    "hygiene": {
        "title": "Password Hygiene Tips",
        "icon":  "🧹",
        "content": """
**Essential password hygiene:**

1️⃣ **Unique password per account** — Never reuse!
2️⃣ **Use a password manager** — Bitwarden, 1Password
3️⃣ **Enable 2FA/MFA** — Even if password leaks
4️⃣ **Check for breaches** — HaveIBeenPwned.com
5️⃣ **Never share passwords** — Not even with IT
6️⃣ **Don't write in plain text** — Use encrypted storage
7️⃣ **Change if compromised** — Not on a schedule
8️⃣ **Use long passphrases** — Easy to type & remember
""",
    },
}

INTERVIEW_QA = [
    {
        "q": "What is password entropy?",
        "a": "Entropy measures unpredictability in bits. "
             "Formula: H = L × log₂(R). Higher entropy = "
             "harder to crack.",
    },
    {
        "q": "What is a rainbow table attack?",
        "a": "Pre-computed table of password→hash mappings. "
             "Countered by password salting before hashing.",
    },
    {
        "q": "What is credential stuffing?",
        "a": "Using leaked username+password pairs from one "
             "breach to try logging into other services. "
             "Prevented by unique passwords + 2FA.",
    },
    {
        "q": "What is NIST SP 800-63B?",
        "a": "NIST's digital identity guidelines. Key points: "
             "length over complexity, check breach lists, "
             "allow all printable characters, support MFA.",
    },
    {
        "q": "Why is 'Password123!' still weak?",
        "a": "It satisfies composition rules (upper, lower, "
             "digit, symbol) but is highly predictable. "
             "Attackers test common patterns like this first.",
    },
    {
        "q": "What is k-anonymity in breach checking?",
        "a": "HaveIBeenPwned API technique: hash password, "
             "send only first 5 chars of hash, get back "
             "matching hashes, check locally. Password never "
             "transmitted!",
    },
]