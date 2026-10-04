"""
pattern_detector.py
Detects weakness patterns in passwords.
"""

import re
import math
from data.common_passwords import (
    KEYBOARD_PATTERNS,
    SEQUENTIAL_PATTERNS,
    COMMON_WORDS,
    LEET_MAP,
)


class PatternDetector:
    """
    Detects various weakness patterns.
    """

    def check_repeated_chars(self, password):
        """Detect repeated characters like 'aaa'."""
        issues = []
        # 3+ same chars in a row
        matches = re.findall(
            r'(.)\1{2,}', password
        )
        if matches:
            issues.append({
                "type":    "REPEATED_CHARS",
                "icon":    "🔄",
                "desc":    f"Repeated characters: "
                           f"{''.join(set(matches))}",
                "penalty": 15,
                "severity":"HIGH",
            })
        # All same char
        if len(set(password)) == 1:
            issues.append({
                "type":    "ALL_SAME",
                "icon":    "⚠️",
                "desc":    "All characters are identical!",
                "penalty": 30,
                "severity":"CRITICAL",
            })
        return issues

    def check_sequential_patterns(self, password):
        """Detect sequences like '123456', 'abcdef'."""
        issues = []
        pw_lower = password.lower()

        for seq in SEQUENTIAL_PATTERNS:
            if seq in pw_lower:
                issues.append({
                    "type":    "SEQUENTIAL",
                    "icon":    "📈",
                    "desc":    f"Sequential pattern: '{seq}'",
                    "penalty": 20,
                    "severity":"HIGH",
                })
                break

        # Detect numeric sequences of 3+
        nums = re.findall(r'\d{3,}', password)
        for n in nums:
            digits  = [int(c) for c in n]
            diffs   = [
                digits[i+1] - digits[i]
                for i in range(len(digits)-1)
            ]
            if len(set(diffs)) == 1 and \
                    diffs[0] in [-1, 0, 1]:
                issues.append({
                    "type":    "NUM_SEQUENCE",
                    "icon":    "🔢",
                    "desc":    f"Numeric sequence: '{n}'",
                    "penalty": 15,
                    "severity":"MEDIUM",
                })
                break

        return issues

    def check_keyboard_patterns(self, password):
        """Detect keyboard walk patterns."""
        issues = []
        pw_lower = password.lower()

        for pattern in KEYBOARD_PATTERNS:
            if pattern in pw_lower:
                issues.append({
                    "type":    "KEYBOARD_WALK",
                    "icon":    "⌨️",
                    "desc":    f"Keyboard pattern: '{pattern}'",
                    "penalty": 20,
                    "severity":"HIGH",
                })
                break

        return issues

    def check_dictionary_words(self, password):
        """Detect common dictionary words."""
        issues = []
        pw_lower = password.lower()

        # Decheetify before checking
        deleeted = pw_lower
        for leet, char in LEET_MAP.items():
            deleeted = deleeted.replace(
                leet, char
            )

        found_words = []
        for word in COMMON_WORDS:
            if word in deleeted and len(word) >= 4:
                found_words.append(word)

        if found_words:
            issues.append({
                "type":    "DICTIONARY",
                "icon":    "📖",
                "desc":    f"Common words found: "
                           f"{', '.join(found_words[:3])}",
                "penalty": 20,
                "severity":"HIGH",
            })

        return issues

    def check_length(self, password):
        """Evaluate password length."""
        issues = []
        length = len(password)

        if length < 8:
            issues.append({
                "type":    "TOO_SHORT",
                "icon":    "📏",
                "desc":    f"Too short ({length} chars). "
                           f"Minimum 8, ideal 16+",
                "penalty": 30,
                "severity":"CRITICAL",
            })
        elif length < 12:
            issues.append({
                "type":    "SHORT",
                "icon":    "📏",
                "desc":    f"Short ({length} chars). "
                           f"Recommend 12+",
                "penalty": 15,
                "severity":"MEDIUM",
            })
        elif length < 16:
            issues.append({
                "type":    "MODERATE_LENGTH",
                "icon":    "📏",
                "desc":    f"Acceptable ({length} chars). "
                           f"16+ is ideal",
                "penalty": 5,
                "severity":"LOW",
            })

        return issues

    def check_char_diversity(self, password):
        """Check character type diversity."""
        issues = []
        has_lower   = bool(re.search(r'[a-z]', password))
        has_upper   = bool(re.search(r'[A-Z]', password))
        has_digit   = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(
            r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?`~]',
            password
        ))

        types = sum([
            has_lower, has_upper,
            has_digit, has_special
        ])

        if types < 2:
            issues.append({
                "type":    "LOW_DIVERSITY",
                "icon":    "🔡",
                "desc":    "Use a mix of character types",
                "penalty": 20,
                "severity":"HIGH",
            })
        elif types < 3:
            issues.append({
                "type":    "MED_DIVERSITY",
                "icon":    "🔡",
                "desc":    "Add more character variety",
                "penalty": 10,
                "severity":"MEDIUM",
            })

        return issues

    def check_dates(self, password):
        """Detect date patterns in passwords."""
        issues = []
        # Match common date formats
        date_patterns = [
            r'\d{2}[/-]\d{2}[/-]\d{2,4}',
            r'\d{4}[/-]\d{2}[/-]\d{2}',
            r'\d{2}\d{2}\d{4}',
            r'\d{4}\d{2}\d{2}',
            r'(19|20)\d{2}',
        ]
        for pat in date_patterns:
            if re.search(pat, password):
                issues.append({
                    "type":    "DATE_PATTERN",
                    "icon":    "📅",
                    "desc":    "Contains date pattern "
                               "(birthday/year)",
                    "penalty": 15,
                    "severity":"MEDIUM",
                })
                break
        return issues

    def check_personal_info(self, password,
                            context=None):
        """Check for personal info overlap."""
        issues = []
        if not context:
            return issues

        pw_lower = password.lower()
        for key, val in context.items():
            if val and len(str(val)) >= 3:
                if str(val).lower() in pw_lower:
                    issues.append({
                        "type":    "PERSONAL_INFO",
                        "icon":    "👤",
                        "desc":    f"Contains your {key}!",
                        "penalty": 25,
                        "severity":"CRITICAL",
                    })
        return issues

    def detect_all(self, password,
                   context=None):
        """Run all pattern checks."""
        all_issues = []
        all_issues += self.check_length(password)
        all_issues += self.check_repeated_chars(
            password
        )
        all_issues += self.check_sequential_patterns(
            password
        )
        all_issues += self.check_keyboard_patterns(
            password
        )
        all_issues += self.check_dictionary_words(
            password
        )
        all_issues += self.check_char_diversity(
            password
        )
        all_issues += self.check_dates(password)
        all_issues += self.check_personal_info(
            password, context
        )
        return all_issues

    def get_total_penalty(self, issues):
        """Sum all penalties."""
        return sum(i.get("penalty", 0)
                   for i in issues)