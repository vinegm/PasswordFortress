import bcrypt


def KDF(password, salt):
    DESIRED_KEY_LENGTH = 32
    ITERATIONS = 2_500  # Make it 10_000 if you don't care about long logins

    derived_key = bcrypt.kdf(password = password.encode(),
                             salt = salt,
                             desired_key_bytes = DESIRED_KEY_LENGTH,
                             rounds = ITERATIONS)

    return derived_key
