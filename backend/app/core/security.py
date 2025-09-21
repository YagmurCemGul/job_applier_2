import os
import keyring
from cryptography.fernet import Fernet, InvalidToken

# Define a constant for the service name used in the keyring
KEYRING_SERVICE_NAME = "autoapply_assistant"
ENCRYPTION_KEY_USERNAME = "encryption_key"

def get_or_create_encryption_key() -> bytes:
    """
    Retrieves the encryption key from the OS keychain.
    If it doesn't exist, a new one is created and stored.

    Returns:
        bytes: The 256-bit (32-byte) encryption key.
    """
    key = keyring.get_password(KEYRING_SERVICE_NAME, ENCRYPTION_KEY_USERNAME)
    if key is None:
        # Generate a new key if one isn't found
        key = Fernet.generate_key()
        keyring.set_password(KEYRING_SERVICE_NAME, ENCRYPTION_KEY_USERNAME, key.decode('utf-8'))
        return key
    return key.encode('utf-8')

# Initialize a Fernet instance with the key
# This key will be loaded once when the module is imported.
_encryption_key = get_or_create_encryption_key()
_cipher_suite = Fernet(_encryption_key)

def encrypt_data(data: str) -> bytes:
    """
    Encrypts a string using the application's encryption key.

    Args:
        data (str): The plaintext string to encrypt.

    Returns:
        bytes: The encrypted data.
    """
    if not isinstance(data, str):
        raise TypeError("Data to encrypt must be a string.")

    return _cipher_suite.encrypt(data.encode('utf-8'))

def decrypt_data(encrypted_data: bytes) -> str:
    """
    Decrypts data using the application's encryption key.

    Args:
        encrypted_data (bytes): The encrypted data to decrypt.

    Returns:
        str: The decrypted plaintext string.
    """
    try:
        decrypted_bytes = _cipher_suite.decrypt(encrypted_data)
        return decrypted_bytes.decode('utf-8')
    except InvalidToken:
        # This can happen if the key is wrong or the data is corrupted
        raise ValueError("Decryption failed. Invalid token or key.")
    except Exception as e:
        # Handle other potential decryption errors
        raise IOError(f"An error occurred during decryption: {e}")

def save_api_key(service_name: str, api_key: str):
    """
    Saves an API key to the OS keychain.

    Args:
        service_name (str): The name of the service (e.g., 'openai', 'google').
        api_key (str): The API key to store.
    """
    keyring.set_password(KEYRING_SERVICE_NAME, service_name, api_key)

def get_api_key(service_name: str) -> str | None:
    """
    Retrieves an API key from the OS keychain.

    Args:
        service_name (str): The name of the service (e.g., 'openai', 'google').

    Returns:
        str | None: The API key if found, otherwise None.
    """
    return keyring.get_password(KEYRING_SERVICE_NAME, service_name)

def delete_api_key(service_name: str):
    """
    Deletes an API key from the OS keychain.

    Args:
        service_name (str): The name of the service to delete.
    """
    try:
        keyring.delete_password(KEYRING_SERVICE_NAME, service_name)
    except keyring.errors.PasswordDeleteError:
        # This error can be raised if the password doesn't exist.
        # We can safely ignore it.
        pass
