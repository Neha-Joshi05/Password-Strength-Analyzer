"""
suggestion_engine.py
Personalized security recommendations engine.
"""

import re


class SuggestionEngine:
    """
    Generates personalized security suggestions
    based on password analysis results.
    """

    def generate(self, analysis):
        """Generate all suggestions."""
        suggestions = []
        issues      = analysis.get("issues", [])
        score       = analysis.get("score", 0)
        length      = analysis.get(
            "password_length", 0
        )
        charset     = analysis.get("charset", {})
        is_common   = analysis.get("is_common", False)

        issue_types = {
            i["type"] for i in issues
        }

        # ── Critical fixes first ──────────────
        if is_common:
            suggestions.append({
                "priority": "CRITICAL",
                "icon":     "🚨",
                "title":    "This password is breached!",
                "detail":   "This exact password appears in "
                            "known data breaches. Change it "
                            "immediately on all accounts.",
                "color":    "#ff0040",
            })

        if "TOO_SHORT" in issue_types:
            suggestions.append({
                "priority": "CRITICAL",
                "icon":     "📏",
                "title":    "Increase length to 12+ chars",
                "detail":   "Length is the single most "
                            "important factor. Each extra "
                            "character multiplies crack time "
                            "exponentially.",
                "color":    "#ff0040",
            })

        if "ALL_SAME" in issue_types:
            suggestions.append({
                "priority": "CRITICAL",
                "icon":     "🔄",
                "title":    "Avoid all-identical characters",
                "detail":   "Passwords like 'aaaaaaa' are "
                            "trivially cracked in milliseconds.",
                "color":    "#ff0040",
            })

        if "PERSONAL_INFO" in issue_types:
            suggestions.append({
                "priority": "CRITICAL",
                "icon":     "👤",
                "title":    "Remove personal information",
                "detail":   "Attackers try names, birthdays, "
                            "and phone numbers first in "
                            "targeted attacks.",
                "color":    "#ff0040",
            })

        # ── High priority ─────────────────────
        if "KEYBOARD_WALK" in issue_types:
            suggestions.append({
                "priority": "HIGH",
                "icon":     "⌨️",
                "title":    "Avoid keyboard patterns",
                "detail":   "Patterns like 'qwerty', 'asdf' "
                            "are in every attacker's wordlist. "
                            "They add zero real security.",
                "color":    "#ff6b00",
            })

        if "SEQUENTIAL" in issue_types or \
                "NUM_SEQUENCE" in issue_types:
            suggestions.append({
                "priority": "HIGH",
                "icon":     "📈",
                "title":    "Remove sequential patterns",
                "detail":   "'12345', 'abcde' sequences are "
                            "trivially guessed. Use random "
                            "combinations instead.",
                "color":    "#ff6b00",
            })

        if "DICTIONARY" in issue_types:
            suggestions.append({
                "priority": "HIGH",
                "icon":     "📖",
                "title":    "Avoid dictionary words",
                "detail":   "Common words (even with "
                            "leet-speak like '3' for 'e') "
                            "are checked by attackers. Mix "
                            "unrelated words or use nonsense.",
                "color":    "#ff6b00",
            })

        if "REPEATED_CHARS" in issue_types:
            suggestions.append({
                "priority": "HIGH",
                "icon":     "🔄",
                "title":    "Reduce repeated characters",
                "detail":   "Repeating 'aaa' or '111' "
                            "significantly reduces entropy. "
                            "Use varied characters.",
                "color":    "#ff6b00",
            })

        # ── Medium priority ───────────────────
        if not charset.get("special"):
            suggestions.append({
                "priority": "MEDIUM",
                "icon":     "✨",
                "title":    "Add special characters",
                "detail":   "Adding symbols like !@#$% "
                            "expands your character pool "
                            "from 62 to 94+, making brute "
                            "force exponentially harder.",
                "color":    "#ffff00",
            })

        if not charset.get("uppercase"):
            suggestions.append({
                "priority": "MEDIUM",
                "icon":     "🔠",
                "title":    "Mix uppercase letters",
                "detail":   "Adding uppercase letters "
                            "doubles the character pool "
                            "for alphabetic characters.",
                "color":    "#ffff00",
            })

        if not charset.get("digits"):
            suggestions.append({
                "priority": "MEDIUM",
                "icon":     "🔢",
                "title":    "Include numbers",
                "detail":   "Numbers add to your character "
                            "pool. Place them randomly, "
                            "not just at the end.",
                "color":    "#ffff00",
            })

        if "DATE_PATTERN" in issue_types:
            suggestions.append({
                "priority": "MEDIUM",
                "icon":     "📅",
                "title":    "Remove date patterns",
                "detail":   "Dates are easily guessed, "
                            "especially birthdays. Attackers "
                            "commonly try personal dates.",
                "color":    "#ffff00",
            })

        if length < 16 and score >= 40:
            suggestions.append({
                "priority": "MEDIUM",
                "icon":     "📏",
                "title":    "Push for 16+ characters",
                "detail":   "At 16 chars with good variety, "
                            "crack time jumps to centuries "
                            "even on modern hardware.",
                "color":    "#ffff00",
            })

        # ── Good practices ────────────────────
        if score >= 60:
            suggestions.append({
                "priority": "TIP",
                "icon":     "💡",
                "title":    "Consider a passphrase",
                "detail":   "4+ random unrelated words "
                            "(e.g., 'Coffee-Brick-Dance-Moon') "
                            "= high entropy + memorable!",
                "color":    "#00d4ff",
            })

        suggestions.append({
            "priority": "TIP",
            "icon":     "🔑",
            "title":    "Use a Password Manager",
            "detail":   "Tools like Bitwarden, 1Password "
                        "generate & store truly random "
                        "unique passwords for every site.",
            "color":    "#00d4ff",
        })

        if score >= 70:
            suggestions.append({
                "priority": "TIP",
                "icon":     "🛡️",
                "title":    "Enable 2FA for extra security",
                "detail":   "Two-Factor Authentication "
                            "protects you even if your "
                            "password is somehow leaked.",
                "color":    "#00ff88",
            })

        return suggestions

    def get_passphrase_example(self):
        """Generate a passphrase example."""
        import random
        words = [
            "Coffee","Rocket","Bridge","Penguin",
            "Sunset","Marble","Jacket","Thunder",
            "Cactus","Lantern","Pickle","Velvet",
            "Cobalt","Frenzy","Quartz","Mystic",
            "Blaze","Storm","Neon","Cipher",
        ]
        chosen = random.sample(words, 4)
        seps   = ["-","_","!","@","#"]
        sep    = random.choice(seps)
        return sep.join(chosen)