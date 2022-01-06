import secrets
import string


def generation_sn(length=10):
    """
    generate sn with combination of
    Uppercase Alphabet and numbers 1 - 9
    """
    return "".join(secrets.choice(string.ascii_uppercase + string.digits[1:]) for _ in range(length))