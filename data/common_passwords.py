"""
common_passwords.py
Top common/breached passwords database.
Used for breach simulation & weak password detection.
⚠️ For DEFENSIVE educational purposes only.
"""

# Top 200 most common passwords (anonymized for safety)
COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678",
    "12345", "1234567", "1234567890", "qwerty",
    "abc123", "111111", "password1", "iloveyou",
    "admin", "letmein", "monkey", "1234",
    "dragon", "master", "sunshine", "princess",
    "welcome", "shadow", "superman", "michael",
    "football", "baseball", "soccer", "hockey",
    "batman", "starwars", "pass", "test",
    "hello", "charlie", "donald", "password123",
    "qwerty123", "1q2w3e4r", "trustno1",
    "rockyou", "google", "login", "admin123",
    "root", "toor", "pass123", "user",
    "hunter2", "whatever", "freedom", "nothing",
    "qazwsx", "zxcvbnm", "asdfgh", "asdfghjkl",
    "qwertyuiop", "lkjhgfds", "poiuytrewq",
    "abc", "abcd", "abcdef", "abcdefg",
    "changeme", "secret", "god", "love",
    "sex", "money", "star", "fire",
    "earth", "water", "hello123", "test123",
    "india", "pakistan", "america", "london",
    "password!", "P@ssword", "P@ssw0rd",
    "Passw0rd", "Password1", "Admin@123",
    "Welcome1", "Welcome@1", "India@123",
    "Computer1", "Internet1", "Mobile@123",
    "Summer2024", "Winter2024", "Spring2024",
    "January1", "February1", "December1",
    "Monday1", "Sunday1", "Saturday1",
    "pass@123", "pass@1234", "password@1",
    "mypassword", "mypass", "passwd",
    "passpass", "123123", "121212",
    "654321", "987654", "147258",
    "258369", "741852", "159357",
    "qweasdzxc", "asdqwezxc", "123qwe",
    "iloveyou1", "fuckyou", "soccer123",
}

# Common keyboard patterns
KEYBOARD_PATTERNS = [
    "qwerty", "qwertyuiop", "asdfgh",
    "asdfghjkl", "zxcvbn", "zxcvbnm",
    "1qaz2wsx", "qazwsx", "1q2w3e",
    "1q2w3e4r", "q1w2e3r4", "!qaz@wsx",
    "qwe123", "123qwe", "asd123",
    "zxc123", "qweasd", "asdzxc",
    "poiuyt", "lkjhgf", "mnbvcx",
]

# Common sequential patterns
SEQUENTIAL_PATTERNS = [
    "abcdef", "bcdefg", "cdefgh",
    "defghi", "efghij", "fedcba",
    "123456", "234567", "345678",
    "456789", "567890", "987654",
    "876543", "765432", "654321",
]

# Common words found in passwords
COMMON_WORDS = [
    "password", "pass", "secret",
    "admin", "user", "login",
    "welcome", "hello", "test",
    "love", "god", "money",
    "india", "home", "work",
    "computer", "internet", "mobile",
    "summer", "winter", "spring",
    "monday", "sunday", "january",
    "sunshine", "dragon", "master",
    "shadow", "freedom", "monkey",
    "football", "baseball", "soccer",
]

# Personal info patterns
PERSONAL_PATTERNS = [
    "name", "birthday", "birth",
    "dob", "phone", "mobile",
    "email", "city", "street",
    "school", "college", "company",
]

# Leetspeak substitutions
LEET_MAP = {
    "@": "a", "4": "a", "3": "e",
    "1": "i", "!": "i", "0": "o",
    "5": "s", "$": "s", "7": "t",
    "+": "t", "9": "g", "6": "g",
}