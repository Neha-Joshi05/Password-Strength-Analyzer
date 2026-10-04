# 🔐 Password Strength Analyzer & Security Suggestion Tool

> **A defensive cybersecurity tool that evaluates password strength in real-time, detects 15+ weakness patterns, calculates entropy, simulates breach checks and provides personalized security recommendations — with a stunning Techno Neon Cyberpunk UI!**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Defensive-green)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-purple)
![NIST](https://img.shields.io/badge/NIST-SP800--63B-orange)
![Deployed](https://img.shields.io/badge/Deployed-Streamlit%20Cloud-brightgreen)

---

## ⚠️ Ethical Disclaimer

> This is a **DEFENSIVE** cybersecurity educational tool.
> - ✅ Passwords analyzed **locally in-memory only**
> - ✅ **No passwords stored, logged or transmitted**
> - ✅ Uses **synthetic/demo** data for testing
> - ✅ Built for **education and awareness**
> - ❌ NOT a password cracker or offensive tool

---

## 🌐 Live Demo

🔗 **[password-analyzer.streamlit.app](https://password-strength-analyzer-zyu7pqn4cuxj4bu9nf3pbz.streamlit.app/)**

---

## 📌 Project Overview

A complete **Password Security Analysis Platform** that includes:
- 🔍 **Real-time Strength Analysis** — Instant scoring
- 📏 **Length Analysis** — Primary strength factor
- 🔡 **Character Diversity** — Pool size calculation
- 🎲 **Entropy Engine** — H = L × log₂(R)
- 🔄 **Pattern Detector** — 8 weakness categories
- 📖 **Common Password Check** — 200+ known passwords
- 💥 **Breach Simulation** — k-Anonymity demo
- 💡 **Suggestion Engine** — Personalized fixes
- 🔑 **Password Generator** — Secure + passphrase
- 📊 **Security Radar** — Visual score breakdown
- 📚 **Education Center** — NIST, entropy, attacks
- 🎤 **Interview Prep** — Cybersecurity Q&A
- 🌙 **Techno Neon UI** — Cyberpunk dark theme
- 📋 **6-Page Interactive Dashboard**

---

## 🗂️ Folder Structure

```
Password-Strength-Analyzer/
├── src/
│   ├── __init__.py
│   ├── analyzer.py              # Core analysis engine
│   ├── pattern_detector.py      # 8 pattern checks
│   ├── entropy_engine.py        # Entropy calculator
│   ├── suggestion_engine.py     # Security recommendations
│   ├── password_generator.py    # Secure generator
│   ├── breach_checker.py        # Breach simulation
│   └── education.py             # Security content
├── data/
│   └── common_passwords.py      # Common password DB
├── tests/
│   └── test_analyzer.py         # Unit tests
├── reports/                     # Generated reports
├── assets/                      # Images & assets
├── dashboard.py                 # Streamlit dashboard
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Data | Pandas, NumPy |
| Hashing | SHA-256, SHA-1 (hashlib) |
| Pattern Detection | Regex (re module) |
| Password Generation | Python secrets module |
| Deploy | Streamlit Cloud |

---

## 🔬 Analysis Engine

### Scoring Formula
```
Score = Base(length) + Diversity + Entropy
        - Pattern Penalties

NOT just: uppercase + lowercase + digit + symbol
EMPHASIS: Length + Unpredictability +
          Pattern Resistance + Context
```

### Entropy Formula
```
H = L × log₂(R)
Where:
  H = Entropy (bits)
  L = Password Length
  R = Character Pool Size

Interpretation:
< 28 bits  → Very Weak
28-35 bits → Weak
36-59 bits → Moderate
60-127 bits→ Strong
128+ bits  → Very Strong
```

### Crack Time (10 Billion guesses/sec GPU)
```
< 28 bits  → Instant
28-40 bits → Minutes to Hours
40-60 bits → Days to Months
60-80 bits → Years to Centuries
80+ bits   → Millions of years 🔐
```

---

## 🕵️ Pattern Detection (15+ Checks)

| Check | Example | Penalty |
|-------|---------|---------|
| Too Short | `abc` | -30 pts |
| Repeated Chars | `aaaa111` | -15 pts |
| Sequential | `123456` | -20 pts |
| Keyboard Walk | `qwerty` | -20 pts |
| Dictionary Word | `password` | -20 pts |
| Low Diversity | `abcdefgh` | -20 pts |
| Date Pattern | `19/05/2002` | -15 pts |
| Personal Info | Your name/city | -25 pts |
| Common Password | `admin123` | -50 pts |
| Leet-speak Variant | `p@ssw0rd` | -25 pts |

---

## 📊 Dashboard Pages

| Page | Features |
|------|---------|
| 🔍 Analyzer | Real-time analysis, 15+ checks, charts, entropy |
| 🔑 Generator | Password, passphrase, batch generate |
| 💥 Breach Sim | Breach check + k-anonymity demo |
| 📚 Education | NIST SP 800-63B, entropy, attacks, hygiene |
| 📊 History | Session score tracking (no passwords stored) |
| 🎤 Interview | Cybersecurity Q&A prep |

---

## 🔒 Security Design

```
Privacy-First Architecture:
├── ✅ All analysis in-memory only
├── ✅ No passwords stored anywhere
├── ✅ No network requests for passwords
├── ✅ SHA-256 hash shown partially (education)
├── ✅ k-Anonymity demonstrated (HIBP method)
├── ✅ Session history = metadata only
└── ✅ Synthetic passwords for testing

HIBP k-Anonymity (Simulated):
1. Hash password locally with SHA-1
2. Send ONLY first 5 chars of hash to API
3. API returns list of matching suffixes
4. Check locally — password NEVER sent!
```

---

## 🏆 Strength Classifications

| Score | Label | Color | Crack Time |
|-------|-------|-------|-----------|
| 0-20 | 💀 VERY WEAK | 🔴 Red | Instant |
| 20-40 | ⚠️ WEAK | 🟠 Orange | Minutes |
| 40-60 | 🟡 MODERATE | 🟡 Yellow | Days |
| 60-80 | ✅ STRONG | 🟢 Green | Years |
| 80-100 | 🛡️ VERY STRONG | 🔵 Cyan | Centuries |

---

## 🚀 Getting Started

```bash
# Clone
git clone https://github.com/Neha-Joshi05/Password-Strength-Analyzer.git
cd Password-Strength-Analyzer

# Setup
python -m venv venv
venv\Scripts\activate

# Install
pip install -r requirements.txt

# Run
python -m streamlit run dashboard.py
```

Open: **http://localhost:8501**

---

## 💡 Password Security Tips (NIST SP 800-63B)

```
✅ DO:
→ Use 16+ characters
→ Use passphrases (4+ random words)
→ Use a password manager
→ Enable 2FA/MFA
→ Use unique passwords per account
→ Check HaveIBeenPwned.com

❌ DON'T:
→ Use personal information
→ Reuse passwords
→ Use keyboard walks (qwerty)
→ Use dictionary words
→ Use sequential numbers (123456)
→ Add just "1!" to meet requirements
```

---

## 🎓 Learning Outcomes

- Password security fundamentals
- Entropy calculation (H = L × log₂(R))
- Pattern detection algorithms
- k-Anonymity breach checking
- NIST SP 800-63B guidelines
- Cryptographic hashing (SHA-256)
- Regex pattern matching
- Secure random generation (secrets module)
- Security dashboard development
- Cloud deployment

---

## 🎤 Interview Topics Covered

- What is password entropy?
- What is a rainbow table attack?
- What is credential stuffing?
- What is NIST SP 800-63B?
- Why is 'Password123!' still weak?
- What is k-anonymity in breach checking?

---

## 👤 Author

**Neha Joshi**
- GitHub: [@Neha-Joshi05](https://github.com/Neha-Joshi05/Password-Strength-Analyzer.git)
- LinkedIn: [neha-joshi-0851a2322](https://www.linkedin.com/in/neha-joshi-0851a2322?utm_source=share_via&utm_content=profile&utm_medium=member_android)

---
