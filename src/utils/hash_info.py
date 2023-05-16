import hashlib


def hash_info(*input: any) -> list:
    """Takes a paramater and hashed it using the hash function blake2b

    Parameters:
    input(any): Value to be hashed

    Returns:
    hashed_data(list): The hashed results from the input
    """
    hashed_data = []
    for data in input:
        hashed_data.append(hashlib.sha256(data.encode()).hexdigest)

    return hashed_data
