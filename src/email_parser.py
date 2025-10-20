def extract_domain(email: str) -> str:
    try:
        return email.split('@')[1]
    except (IndexError, AttributeError):
        return None


def extract_company_name(domain: str) -> str:
    if not domain:
        return None
    return domain.split('.')[0].capitalize()
