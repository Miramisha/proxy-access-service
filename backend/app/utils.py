import secrets


def generate_activation_key() -> str:
    return secrets.token_urlsafe(24)