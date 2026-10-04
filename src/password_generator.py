"""
password_generator.py
Secure password and passphrase generator.
"""

import random
import string
import math


class PasswordGenerator:
    """
    Generates cryptographically strong passwords.
    Uses Python's secrets module for randomness.
    """

    WORDLIST = [
        "Apple","Brave","Cloud","Delta","Eagle",
        "Frost","Globe","Haven","Ivory","Jewel",
        "Kite","Lunar","Maple","Noble","Ocean",
        "Prism","Quest","River","Storm","Titan",
        "Ultra","Vivid","Witch","Xenon","Yacht",
        "Zebra","Amber","Blaze","Coral","Dusk",
        "Echo","Flame","Grace","Honor","Index",
        "Jade","Karma","Light","Magic","Nexus",
        "Onyx","Peace","Quick","Ridge","Spike",
        "Torch","Unity","Valor","Windy","Xero",
        "Young","Zippy","Alpha","Beta","Gamma",
        "Delta","Sigma","Theta","Omega","Cyber",
        "Neon","Pixel","Quark","Radar","Solar",
        "Tesla","Ultra","Vapor","Wired","Axiom",
        "Boost","Crypt","Debug","Ether","Force",
    ]

    SPECIAL_SAFE = "!@#$%^&*-_+=?"

    def generate_password(self, length=16,
                          use_upper=True,
                          use_lower=True,
                          use_digits=True,
                          use_special=True,
                          exclude_ambiguous=False):
        """Generate a strong random password."""
        import secrets

        pool = ""
        guaranteed = []

        if use_lower:
            chars = string.ascii_lowercase
            if exclude_ambiguous:
                chars = chars.replace(
                    "l","").replace("o","")
            pool += chars
            guaranteed.append(
                secrets.choice(chars)
            )

        if use_upper:
            chars = string.ascii_uppercase
            if exclude_ambiguous:
                chars = chars.replace(
                    "I","").replace(
                    "O","").replace("L","")
            pool += chars
            guaranteed.append(
                secrets.choice(chars)
            )

        if use_digits:
            chars = string.digits
            if exclude_ambiguous:
                chars = chars.replace(
                    "0","").replace("1","")
            pool += chars
            guaranteed.append(
                secrets.choice(chars)
            )

        if use_special:
            pool += self.SPECIAL_SAFE
            guaranteed.append(
                secrets.choice(self.SPECIAL_SAFE)
            )

        if not pool:
            pool = string.ascii_letters + \
                   string.digits

        # Fill remaining length
        remaining = length - len(guaranteed)
        password  = guaranteed + [
            secrets.choice(pool)
            for _ in range(remaining)
        ]

        # Shuffle to avoid predictable placement
        random.SystemRandom().shuffle(password)
        return "".join(password)

    def generate_passphrase(self, n_words=4,
                             separator="-",
                             capitalize=True,
                             add_number=True):
        """
        Generate a memorable passphrase.
        XKCD-style: 4 random unrelated words.
        """
        import secrets
        words = [
            secrets.choice(self.WORDLIST)
            for _ in range(n_words)
        ]
        if capitalize:
            words = [w.capitalize() for w in words]
        phrase = separator.join(words)
        if add_number:
            phrase += str(
                secrets.randbelow(100)
            )
        return phrase

    def generate_pin(self, length=6):
        """Generate a secure numeric PIN."""
        import secrets
        return "".join(
            str(secrets.randbelow(10))
            for _ in range(length)
        )

    def generate_batch(self, count=5,
                       length=16):
        """Generate multiple passwords."""
        return [
            self.generate_password(length)
            for _ in range(count)
        ]

    def calculate_strength(self, password):
        """Quick strength estimate for display."""
        entropy = len(password) * math.log2(
            max(
                len(set(password)), 1
            )
        )
        return round(entropy, 1)