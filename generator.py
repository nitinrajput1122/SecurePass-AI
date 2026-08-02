import random
import string


def generate_password(
    length=12,
    uppercase=True,
    lowercase=True,
    numbers=True,
    symbols=True
):
    characters = ""

    if uppercase:
        characters += string.ascii_uppercase

    if lowercase:
        characters += string.ascii_lowercase

    if numbers:
        characters += string.digits

    if symbols:
        characters += string.punctuation

    if not characters:
        return ""

    password = "".join(
        random.choice(characters)
        for _ in range(length)
    )

    return password