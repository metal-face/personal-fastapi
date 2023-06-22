import bcrypt

def hash_password(plaintext_password: str) -> bytes:
    bcrypt_password = bcrypt.hashpw(plaintext_password.encode(), bcrypt.gensalt())
    return bcrypt_password


def check_password(password: str, hashword: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashword)