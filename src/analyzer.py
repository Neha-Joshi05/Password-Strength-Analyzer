"""
analyzer.py
Core password strength analysis engine.
Combines all checks into a unified score.
⚠️ DEFENSIVE tool — passwords never stored or logged.
"""

import re
import math
from data.common_passwords import COMMON_PASSWORDS
from src.entropy_engine    import EntropyEngine
from src.pattern_detector  import PatternDetector


class PasswordAnalyzer:
    """
    Main password analysis engine.

    Scoring Philosophy:
    ─────────────────────────────────────
    Score = Base(length) + Diversity +
            Entropy - Penalties
    ─────────────────────────────────────
    NOT just: uppercase + lowercase + digit + symbol
    EMPHASIS: Length + Unpredictability +
              Pattern Resistance + Context
    """

    CLASSIFICATIONS = {
        (0,  20):  ("VERY WEAK",  "#ff0040", "💀", 0),
        (20, 40):  ("WEAK",       "#ff6b00", "⚠️", 1),
        (40, 60):  ("MODERATE",   "#ffff00", "🟡", 2),
        (60, 80):  ("STRONG",     "#00ff88", "✅", 3),
        (80, 101): ("VERY STRONG","#00d4ff", "🛡️", 4),
    }

    def __init__(self):
        self.entropy_engine = EntropyEngine()
        self.pattern_detector= PatternDetector()

    def analyze(self, password, context=None):
        """
        Full password analysis.
        Returns comprehensive security report.
        ⚠️ Password is analyzed in-memory only.
        """
        if not password:
            return self._empty_result()

        # ── Base scoring ──────────────────────
        length  = len(password)
        base    = self._length_score(length)
        div     = self._diversity_score(password)
        entropy = self.entropy_engine\
            .calculate_entropy(password)
        charset = self.entropy_engine\
            .get_charset_breakdown(password)

        # ── Pattern detection ─────────────────
        issues  = self.pattern_detector.detect_all(
            password, context
        )
        penalty = self.pattern_detector\
            .get_total_penalty(issues)

        # ── Common password check ─────────────
        is_common = password.lower() in \
                    COMMON_PASSWORDS
        is_common_variant = self._check_variant(
            password
        )
        if is_common:
            penalty += 50
        elif is_common_variant:
            penalty += 25

        # ── Final score ───────────────────────
        raw_score = base + div + \
                    min(entropy * 0.4, 30)
        final     = max(0, min(100,
                    raw_score - penalty * 0.8
                  ))
        final     = round(final, 1)

        # ── Classification ────────────────────
        label, color, icon, level = \
            self._classify(final)

        # ── Effective entropy ─────────────────
        eff_entropy = self.entropy_engine\
            .calculate_effective_entropy(
                password,
                pattern_penalty=penalty * 0.5,
            )
        crack_time  = self.entropy_engine\
            .get_crack_time(eff_entropy)
        ent_label, ent_color = \
            self.entropy_engine\
            .get_entropy_label(eff_entropy)

        # ── Character analysis ────────────────
        char_analysis = self._char_analysis(password)

        # ── Severity counts ───────────────────
        critical = sum(
            1 for i in issues
            if i.get("severity") == "CRITICAL"
        )
        high     = sum(
            1 for i in issues
            if i.get("severity") == "HIGH"
        )
        medium   = sum(
            1 for i in issues
            if i.get("severity") == "MEDIUM"
        )

        return {
            # Core
            "password_length":    length,
            "score":              final,
            "label":              label,
            "color":              color,
            "icon":               icon,
            "level":              level,
            # Entropy
            "entropy":            entropy,
            "eff_entropy":        eff_entropy,
            "crack_time":         crack_time,
            "entropy_label":      ent_label,
            "entropy_color":      ent_color,
            # Charset
            "charset":            charset,
            # Issues
            "issues":             issues,
            "penalty":            round(penalty, 1),
            "critical_count":     critical,
            "high_count":         high,
            "medium_count":       medium,
            # Flags
            "is_common":          is_common,
            "is_common_variant":  is_common_variant,
            # Character breakdown
            "char_analysis":      char_analysis,
            # Component scores
            "base_score":         round(base, 1),
            "diversity_score":    round(div, 1),
            "raw_score":          round(raw_score, 1),
        }

    def _empty_result(self):
        """Return empty result for blank input."""
        return {
            "password_length": 0,
            "score":           0,
            "label":           "ENTER PASSWORD",
            "color":           "#333",
            "icon":            "🔐",
            "level":           -1,
            "entropy":         0,
            "eff_entropy":     0,
            "crack_time":      "N/A",
            "entropy_label":   "N/A",
            "entropy_color":   "#333",
            "charset":         {},
            "issues":          [],
            "penalty":         0,
            "critical_count":  0,
            "high_count":      0,
            "medium_count":    0,
            "is_common":       False,
            "is_common_variant":False,
            "char_analysis":   {},
            "base_score":      0,
            "diversity_score": 0,
            "raw_score":       0,
        }

    def _length_score(self, length):
        """Score based on length (0-40 pts)."""
        if length == 0:  return 0
        if length < 6:   return 5
        if length < 8:   return 12
        if length < 12:  return 22
        if length < 16:  return 30
        if length < 20:  return 36
        return 40

    def _diversity_score(self, password):
        """Score based on char diversity (0-30 pts)."""
        score = 0
        if re.search(r'[a-z]', password): score += 6
        if re.search(r'[A-Z]', password): score += 6
        if re.search(r'[0-9]', password): score += 6
        if re.search(
            r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?`~]',
            password
        ): score += 9
        if re.search(r'\s', password): score += 3
        return score

    def _classify(self, score):
        """Classify password strength."""
        for (lo, hi), vals in \
                self.CLASSIFICATIONS.items():
            if lo <= score < hi:
                return vals
        return ("VERY WEAK","#ff0040","💀", 0)

    def _check_variant(self, password):
        """Check common password variants."""
        pw = password.lower()
        from data.common_passwords import LEET_MAP
        deleet = pw
        for leet, char in LEET_MAP.items():
            deleet = deleet.replace(leet, char)
        return deleet in COMMON_PASSWORDS

    def _char_analysis(self, password):
        """Detailed character composition."""
        lowercase = len(re.findall(r'[a-z]', password))
        uppercase = len(re.findall(r'[A-Z]', password))
        digits    = len(re.findall(r'[0-9]', password))
        special   = len(re.findall(
            r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?`~]',
            password
        ))
        spaces    = len(re.findall(r'\s', password))
        unique    = len(set(password))
        total     = len(password)

        return {
            "lowercase": lowercase,
            "uppercase": uppercase,
            "digits":    digits,
            "special":   special,
            "spaces":    spaces,
            "unique":    unique,
            "total":     total,
            "unique_pct":round(
                unique/max(total,1)*100, 1
            ),
        }