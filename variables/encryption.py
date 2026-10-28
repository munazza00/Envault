from cryptography.fernet import Fernet
from django.conf import settings


def get_fernet():
    key = settings.ENVAULT_ENCRYPTION_KEY.encode()
    return Fernet(key)


def encrypt_value(value):
    fernet = get_fernet()
    encrypted_value = fernet.encrypt(value.encode())
    return encrypted_value.decode()


def decrypt_value(encrypted_value):
    fernet = get_fernet()
    decrypted_value = fernet.decrypt(encrypted_value.encode())
    return decrypted_value.decode()