import bcrypt


def hash_info(data: str) -> bytes:
    """Takes a paramater and hashed it using the hash function blake2b

    Parameters:
    data(any): Value to be hashed

    Returns:
    hashed_data(bytes): Hashed data
    salt(bytes): Salt used for hashing
    """
    salt = bcrypt.gensalt()
    hashed_data = bcrypt.hashpw(data.encode('utf-8'), salt)

    return hashed_data, salt


def hash_wsalt(data: str, salt: bytes):
    """Hashes a given input with the given salt for checking the password
    
    Parameters:
    data(str): Data that will be hashed
    salt(bytes): Salt that will be used to check the hash

    Returns:
    hashed_data(bytes): Hash made from the data and salt given
    """
    hashed_data = bcrypt.hashpw(data.encode('utf-8'), salt)
    return hashed_data
