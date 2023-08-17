import secrets
import string

SLUG_CHARS = string.ascii_letters + string.digits
SLUG_CHARS_DENIED = '01IloO'


def generate_slug(length=6) -> str:
    slug = ''
    while len(slug) < length:
        char = secrets.choice(SLUG_CHARS)
        if char in SLUG_CHARS_DENIED:
            continue
        slug += char
    return slug
