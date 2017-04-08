from django.test import TestCase, override_settings
from django.utils import six
from django_encrypted_filefield.constants import _get_setting, get_bytes

try:
    from unittest import mock  # Python 3
except ImportError:
    import mock  # Python 2


class ConstantsTestCase(TestCase):

    def test_get_bytes_with_string(self):
        for s in ("a", "α", ""):
            self.assertEqual(get_bytes(s), bytes(s.encode("utf-8")))

    def test_get_bytes_with_nothing(self):
        for s in (None, 0, False, 1, True, lambda _: 1):
            self.assertRaises(TypeError, get_bytes, s)

    def test_get_bytes_with_bytes(self):
        inputs = (
            bytes("a".encode("utf-8")),
            bytes("α".encode("utf-8")),
            bytes("".encode("utf-8"))
        )
        for s in inputs:
            self.assertEqual(get_bytes(s), s)

    @override_settings(DEFF_SALT="salt")
    @override_settings(DEFF_PASSWORD="password")
    @override_settings(DEFF_FETCH_URL_NAME="fetch")
    def test__get_setting_from_settings(self):
        self.assertEqual(_get_setting("SALT"), "salt")
        self.assertEqual(_get_setting("PASSWORD"), "password")
        self.assertEqual(_get_setting("FETCH_URL_NAME"), "fetch")

    def test__get_setting_from_environment(self):
        self.assertEqual(_get_setting("SALT"), "salt")
        self.assertEqual(_get_setting("PASSWORD"), "password")
        self.assertEqual(_get_setting("FETCH_URL_NAME"), "fetch")

    @override_settings(DEFF_SALT="asdf")
    @override_settings(DEFF_PASSWORD="asdf")
    @override_settings(DEFF_FETCH_URL_NAME="asdf")
    def test__get_setting_from_both(self):
        self.assertEqual(_get_setting("SALT"), "salt")
        self.assertEqual(_get_setting("PASSWORD"), "password")
        self.assertEqual(_get_setting("FETCH_URL_NAME"), "fetch")
