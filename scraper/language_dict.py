"""
Language dictionaries for date parsing and text matching
"""

# Date patterns for relative date parsing
DATE_PATTERNS = {
    # French
    'il y a un an': 365, 'il y a 1 an': 365,
    'il y a 2 ans': 365 * 2, 'il y a 3 ans': 365 * 3,
    'il y a un mois': 30, 'il y a 1 mois': 30,
    'il y a 2 mois': 30 * 2, 'il y a 3 mois': 30 * 3,
    'il y a une semaine': 7, 'il y a 1 semaine': 7,
    'il y a 2 semaines': 7 * 2, 'il y a 3 semaines': 7 * 3,
    'il y a un jour': 1, 'il y a 1 jour': 1,
    'il y a 2 jours': 2, 'il y a 3 jours': 3,
    'depuis un an': 365, 'depuis 1 an': 365,
    
    # English
    'a year ago': 365, '1 year ago': 365,
    '2 years ago': 365 * 2, '3 years ago': 365 * 3,
    'a month ago': 30, '1 month ago': 30,
    '2 months ago': 30 * 2, '3 months ago': 30 * 3,
    'a week ago': 7, '1 week ago': 7,
    '2 weeks ago': 7 * 2, '3 weeks ago': 7 * 3,
    'a day ago': 1, '1 day ago': 1,
    '2 days ago': 2, '3 days ago': 3,
}

# Cookie accept button selectors
COOKIE_SELECTORS = [
    "//button[contains(., 'Accept all')]",
    "//button[contains(., 'Tout accepter')]",
    "//button[contains(@aria-label, 'Accept all')]",
    "//button[contains(@class, 'accept')]",
]

# Review button selectors for Google Maps
REVIEW_BUTTONS = [
    "//button[contains(., 'Reviews')]",
    "//button[contains(., 'Avis')]",
    "//button[contains(@aria-label, 'reviews')]",
    "//button[@data-tab-index='1']",
]

# Container selectors for scrollable content
CONTAINER_SELECTORS = [
    '//div[@role="main"]',
    '//div[contains(@class, "m6QErb")]',
    '//div[contains(@jsaction, "scroll")]',
    '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf"]',
]

# Google Maps review element selectors
REVIEW_SELECTORS = [
    '//div[@class="jftiEf fontBodyMedium "]',
    '//div[contains(@class, "jftiEf")]',
    '//div[@data-review-id]',
    '//div[contains(@jsaction, "mouseover")]',
]