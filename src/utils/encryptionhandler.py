from cryptography.fernet import Fernet


def encrypt_data(data: str, key: bytes) -> bytes:
    """Encrypts the given data with the given key
    
    Parameters:
    data(str): Data that will be encrypted
    key(bytes): Key that will be used in the encryption

    Returns:
    encrypted_data(bytes): The encrypted data
    """
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())

    return encrypted_data


def decrypt_data(data: bytes, key: bytes) -> str:
    """decrypts the given data with the given key

    Parameters:
    data(bytes): Data that will be decrypted
    key(bytes): Key that will be used in the dencryption

    Returns:
    encrypted_data(str): The dencrypted data
    """
    cipher = Fernet(key)
    decrypted_data = (cipher.decrypt(data)).decode()

    return decrypted_data
