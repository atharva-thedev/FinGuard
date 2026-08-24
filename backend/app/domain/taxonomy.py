DEFAULT_CATEGORIES = [
    "Travel",
    "Software",
    "Office Supplies",
    "Equipment",
    "Utilities",
    "Professional Services",
    "Other",
]

KEYWORD_MAP = {
    "uber": "Travel",
    "lyft": "Travel",
    "airline": "Travel",
    "aws": "Software",
    "microsoft": "Software",
    "adobe": "Software",
    "staples": "Office Supplies",
    "office depot": "Office Supplies",
    "electric": "Utilities",
    "water": "Utilities",
    "consult": "Professional Services",
    "legal": "Professional Services",
}


def guess_category(vendor_name: str) -> str:
    v = (vendor_name or "").lower()
    for key, cat in KEYWORD_MAP.items():
        if key in v:
            return cat
    return "Other"
