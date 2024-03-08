import secrets

def generate_verification_token():
    return secrets.token_urlsafe(16)