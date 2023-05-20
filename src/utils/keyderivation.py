import bcrypt
import base64


def KDF(password: str, salt: bytes) -> bytes:
    """Derives a key from the user password for encryption
    
    Parameters:
    password(str): Password of the user
    salt(bytes): Salt that will be used in the key derivation

    Returns:
    derived_key(bytes): The derived key from the password and salt
    """
    DESIRED_KEY_LENGTH = 32
    ITERATIONS = 2_500  # Make it 10_000 if you don't care about long logins

    uncoded_derived_key = bcrypt.kdf(password = password.encode(),
                                     salt = salt,
                                     desired_key_bytes = DESIRED_KEY_LENGTH,
                                     rounds = ITERATIONS)
    derived_key = base64.urlsafe_b64encode(uncoded_derived_key)

    return derived_key
