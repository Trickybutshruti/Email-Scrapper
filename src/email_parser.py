# src/email_parser.py

"""
Handles email parsing logic:
- Extract domain from email
- Extract company name from domain
"""

def extract_domain(email: str) -> str:
    """Extracts the domain part of an email (after '@')."""
    try:
        return email.split('@')[1]
    except (IndexError, AttributeError):
        return None


def extract_company_name(domain: str) -> str:
    """Extracts company name (first part before '.') from domain."""
    if not domain:
        return None
    return domain.split('.')[0].capitalize()
