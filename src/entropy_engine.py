"""
entropy_engine.py
Password entropy calculation engine.
Measures unpredictability of passwords.
"""

import math
import re
from data.common_passwords import LEET_MAP


class EntropyEngine:
    """
    Calculates password entropy and unpredictability.

    Entropy Formula:
    H = L × log2(R)
    Where:
    H = Entropy (bits)
    L = Password Length
    R = Character Pool Size

    Entropy Interpretation:
    < 28 bits  → Very Weak
    28-35 bits → Weak
    36-59 bits → Moderate
    60-127 bits→ Strong
    128+ bits  → Very Strong
    """

    def calculate_charset_size(self, password):
        """Calculate the character pool size."""
        pool = 0
        if re.search(r'[a-z]', password):
            pool += 26   # lowercase
        if re.search(r'[A-Z]', password):
            pool += 26   # uppercase
        if re.search(r'[0-9]', password):
            pool += 10   # digits
        if re.search(
            r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?`~]',
            password
        ):
            pool += 32   # special chars
        if re.search(r'\s', password):
            pool += 1    # space
        return max(pool, 1)

    def calculate_entropy(self, password):
        """
        Calculate raw entropy bits.
        H = L × log2(R)
        """
        if not password:
            return 0.0
        pool    = self.calculate_charset_size(password)
        length  = len(password)
        entropy = length * math.log2(pool)
        return round(entropy, 2)

    def calculate_effective_entropy(self, password,
                                    pattern_penalty=0,
                                    common_penalty=0):
        """
        Effective entropy after penalties.
        Accounts for patterns and common words.
        """
        raw     = self.calculate_entropy(password)
        penalty = pattern_penalty + common_penalty
        return max(0.0, round(raw - penalty, 2))

    def get_crack_time(self, entropy):
        """
        Estimate crack time based on entropy.
        Assumes 10 billion guesses/second (GPU).
        """
        if entropy <= 0:
            return "Instant"

        guesses = 2 ** entropy
        # 10^10 guesses per second (GPU attack)
        seconds = guesses / (10 ** 10)

        if seconds < 0.001:
            return "Instant ⚡"
        elif seconds < 1:
            return f"{seconds*1000:.1f} milliseconds"
        elif seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} hours"
        elif seconds < 2592000:
            return f"{seconds/86400:.1f} days"
        elif seconds < 31536000:
            return f"{seconds/2592000:.1f} months"
        elif seconds < 3153600000:
            return f"{seconds/31536000:.1f} years"
        elif seconds < 315360000000:
            return f"{seconds/31536000/100:.0f} centuries"
        else:
            return "Millions of years 🔐"

    def get_entropy_label(self, entropy):
        """Get human-readable entropy label."""
        if entropy < 28:
            return "Very Low", "#ff0040"
        elif entropy < 36:
            return "Low", "#ff6b00"
        elif entropy < 60:
            return "Moderate", "#ffff00"
        elif entropy < 128:
            return "High", "#00ff88"
        else:
            return "Very High", "#00d4ff"

    def get_charset_breakdown(self, password):
        """Get character set breakdown."""
        return {
            "lowercase": bool(
                re.search(r'[a-z]', password)
            ),
            "uppercase": bool(
                re.search(r'[A-Z]', password)
            ),
            "digits":    bool(
                re.search(r'[0-9]', password)
            ),
            "special":   bool(
                re.search(
                    r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?`~]',
                    password
                )
            ),
            "space":     bool(
                re.search(r'\s', password)
            ),
            "pool_size": self.calculate_charset_size(
                password
            ),
        }

    def decheetify(self, password):
        """Remove leetspeak substitutions."""
        result = password.lower()
        for leet, char in LEET_MAP.items():
            result = result.replace(leet, char)
        return result