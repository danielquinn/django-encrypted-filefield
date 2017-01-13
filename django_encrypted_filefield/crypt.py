import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from django.conf import settings


class Cryptographer(object):

    @classmethod
    def _get_fernet(cls):
        return Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=settings.DEFF_SALT,
            iterations=100000,
            backend=default_backend()
        ).derive(settings.DEFF_PASSWORD)))

    @classmethod
    def encrypted(cls, content):
        return cls._get_fernet().encrypt(content)

    @classmethod
    def decrypted(cls, content):
        return cls._get_fernet().decrypt(content)
