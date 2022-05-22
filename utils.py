import hashlib


def hash_password(password):
    d = hashlib.sha3_256(password.encode())
    return d.hexdigest()
