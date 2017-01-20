import os

from django.conf import settings


def get_bytes(name):
    r = os.getenv("DEFF_{}".format(name))
    if r:
        return bytes(r.encode("utf-8"))
    return None

SALT = get_bytes("SALT") or getattr(settings, 'DEFF_SALT', None)
PASSWORD = get_bytes("PASSWORD") or getattr(settings, 'DEFF_PASSWORD', None)
FETCH_URL_NAME = os.getenv("DEFF_FETCH_URL_NAME") or getattr(settings, 'DEFF_FETCH_URL_NAME', None)
