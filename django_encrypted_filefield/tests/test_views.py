from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

try:
    from unittest import mock  # Python 3
except ImportError:
    import mock  # Python 2


class ViewsTestCase(TestCase):

    GIF = (
        b'GIF87a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff,\x00\x00'
        b'\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    )
    ENCRYPTED_GIF = (
        b'gAAAAABYdqQ9WGU1wl8-wZ98LLKwiTcly3zseV70K2gVobCdTdvWDyXQBSbE6ZDaC6xi'
        b'pqH6pIC4TZWvuY3eW0PhT-JfxtahcCye_eqpGLYT_7Vxw0vMr1aZdGrz4Wn8FGWcFn8y'
        b'v2ai'
    )

    @override_settings(DEFF_FETCH_URL_NAME="fetch")
    @override_settings(MEDIA_ROOT="/tmp")
    def test_path_starts_media_root(self):
        kwargs = {"path": "/etc/passwd"}
        self.assertEqual(
            self.client.get(reverse("fetch", kwargs=kwargs)).status_code, 404)

    @override_settings(DEFF_FETCH_URL_NAME="fetch")
    def test_path_does_not_exist(self):
        kwargs = {"path": "this/file/does/not/exist"}
        self.assertEqual(
            self.client.get(reverse("fetch", kwargs=kwargs)).status_code, 404)

    @override_settings(DEFF_FETCH_URL_NAME="fetch")
    @mock.patch("django_encrypted_filefield.views.os.path.exists")
    @mock.patch(
        "django_encrypted_filefield.views.open",
        mock.mock_open(read_data=ENCRYPTED_GIF),
        create=True
    )
    def test_local_path_exists(self, exists):
        exists.return_value = True
        kwargs = {"path": "dummy-file"}
        response = self.client.get(reverse("fetch", kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.GIF)
        self.assertEqual(response["Content-Type"], "image/gif")
