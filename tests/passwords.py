# должно пройти

import random
import string

def generate_password(length=8):
    if length < 4:
        return "Password length must be at least 4."
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

if __name__ == "__main__":
    print(generate_password(12))
