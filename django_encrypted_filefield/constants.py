import os
from django.conf import settings


def _get_setting(name):
    setting_name = "DEFF_{}".format(name)
    return os.getenv(setting_name, getattr(settings, setting_name, None))


def get_bytes(v):
    if v:
        return bytes(v.encode("utf-8"))
    return None


SALT = get_bytes(_get_setting("SALT"))
PASSWORD = get_bytes(_get_setting("PASSWORD"))
FETCH_URL_NAME = _get_setting("FETCH_URL_NAME")
