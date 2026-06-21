import bcrypt


def hash_password(password):
    password_bytes = password.encode()

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode()


def verify_password(
        password,
        hashed_password):

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )