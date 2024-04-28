import secrets


def token_gen():
    return secrets.token_urlsafe()


print(token_gen())