import string
import random

def generate_token():
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(24))