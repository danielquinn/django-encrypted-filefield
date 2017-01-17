import os


def get_bytes(name):
    r = os.getenv("DEFF_{}".format(name))
    if r:
        return bytes(r.encode("utf-8"))
    return None


SALT = get_bytes("SALT")
PASSWORD = get_bytes("PASSWORD")
FETCH_URL_NAME = os.getenv("DEFF_FETCH_URL_NAME")
