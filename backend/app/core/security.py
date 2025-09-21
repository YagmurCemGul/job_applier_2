import os
import keyring
import json
from cryptography.fernet import Fernet, InvalidToken

# Define a constant for the service name used in the keyring for the app itself
KEYRING_APP_SERVICE = "autoapply_assistant_app"
ENCRYPTION_KEY_USERNAME = "encryption_key"

# --- Data Encryption Functions (for local DB) ---

def get_or_create_encryption_key() -> bytes:
    """
    Retrieves the data encryption key from the OS keychain.
    If it doesn't exist, a new one is created and stored.
    """
    key = keyring.get_password(KEYRING_APP_SERVICE, ENCRYPTION_KEY_USERNAME)
    if key is None:
        key = Fernet.generate_key()
        keyring.set_password(KEYRING_APP_SERVICE, ENCRYPTION_KEY_USERNAME, key.decode('utf-8'))
        return key
    return key.encode('utf-8')

_encryption_key = get_or_create_encryption_key()
_cipher_suite = Fernet(_encryption_key)

def encrypt_data(data: str) -> bytes:
    """Encrypts a string."""
    return _cipher_suite.encrypt(data.encode('utf-8'))

def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypts data."""
    try:
        decrypted_bytes = _cipher_suite.decrypt(encrypted_data)
        return decrypted_bytes.decode('utf-8')
    except InvalidToken:
        raise ValueError("Decryption failed. Invalid token or key.")

# --- AI Service Credential Management Functions ---

def save_credential(service_name: str, username: str, password: str):
    """
    Saves a credential (username and password) to the OS keychain.
    The service_name acts as the service identifier, and the username
    is the key for the password.
    """
    # Keyring stores a "password" for a "service" and "username".
    # Here, 'service_name' is our service (e.g., "openai"),
    # 'username' is the user's login for that service,
    # and 'password' is the user's password for that service.
    keyring.set_password(service_name, username, password)

def get_credential(service_name: str, username: str) -> str | None:
    """
    Retrieves a password for a given service and username from the OS keychain.
    """
    return keyring.get_password(service_name, username)

def get_all_credentials_for_service(service_name: str) -> list[dict]:
    """
    This is a conceptual challenge. Keyring doesn't typically allow listing
    all usernames for a service for security reasons. The app will need to
    store the usernames (not passwords) in its own local DB to know which
    credentials it has stored.

    For now, this function is a placeholder. The UI will need to manage this state.
    """
    # In a real app, you'd query your local DB for saved usernames for a service
    # and then check keyring for each one.
    print(f"Warning: Listing all credentials is not directly supported by keyring. App needs to store usernames.")
    return []


def delete_credential(service_name: str, username: str):
    """
    Deletes a specific credential from the OS keychain.
    """
    try:
        keyring.delete_password(service_name, username)
    except keyring.errors.PasswordDeleteError:
        # This error can be raised if the password doesn't exist. Safely ignore.
        pass
