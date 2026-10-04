"""
breach_checker.py
Simulates breach database check.
⚠️ LOCAL SIMULATION ONLY — no data transmitted.
In production: use HaveIBeenPwned k-anonymity API.
"""

import hashlib
import random
from data.common_passwords import COMMON_PASSWORDS


class BreachChecker:
    """
    Simulates password breach database.

    Real-world implementation uses:
    HaveIBeenPwned API with k-anonymity:
    1. Hash password with SHA-1
    2. Send first 5 chars of hash
    3. API returns matching hashes
    4. Check locally — password NEVER sent!

    This simulation:
    - Checks against known common passwords
    - Shows how breach checking works
    - Never stores or transmits passwords
    """

    # Simulated breach count database
    BREACH_COUNTS = {
        pw: random.randint(100, 23_000_000)
        for pw in COMMON_PASSWORDS
    }

    def check_password(self, password):
        """
        Check if password appears in breaches.
        Returns breach info dict.
        """
        pw_lower = password.lower()

        # Direct match
        if pw_lower in COMMON_PASSWORDS:
            count = self.BREACH_COUNTS.get(
                pw_lower,
                random.randint(1000, 100000)
            )
            return {
                "found":   True,
                "count":   count,
                "type":    "EXACT_MATCH",
                "message": f"Found in {count:,} "
                           f"breach records!",
                "color":   "#ff0040",
                "icon":    "🚨",
            }

        # Variant check
        from data.common_passwords import LEET_MAP
        deleet = pw_lower
        for leet, char in LEET_MAP.items():
            deleet = deleet.replace(leet, char)

        if deleet in COMMON_PASSWORDS:
            return {
                "found":   True,
                "count":   random.randint(
                    1000, 500000
                ),
                "type":    "VARIANT_MATCH",
                "message": "Leet-speak variant "
                           "found in breaches!",
                "color":   "#ff6b00",
                "icon":    "⚠️",
            }

        return {
            "found":   False,
            "count":   0,
            "type":    "NOT_FOUND",
            "message": "Not found in known "
                       "breach database ✓",
            "color":   "#00ff88",
            "icon":    "✅",
        }

    def get_hash_preview(self, password):
        """
        Show SHA-256 hash preview.
        Educational: demonstrates hashing.
        """
        if not password:
            return "—"
        h = hashlib.sha256(
            password.encode()
        ).hexdigest()
        # Show only partial hash
        return h[:8] + "..." + h[-8:]

    def simulate_api_call(self, password):
        """
        Simulate k-anonymity API process.
        Educational demonstration.
        """
        sha1 = hashlib.sha1(
            password.encode()
        ).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        return {
            "sha1_prefix": prefix,
            "sha1_suffix": f"{suffix[:8]}...",
            "full_hash":   sha1[:16] + "...",
            "description": (
                f"Send '{prefix}' to HIBP API → "
                f"Get list → Check locally"
            ),
        }