from unittest import mock

from django.test import TestCase, override_settings
from django.urls import reverse


class ViewsTestCase(TestCase):

    GIF = (
        b"GIF87a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff,\x00\x00"
        b"\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    )
    ENCRYPTED_GIF = (
        b"gAAAAABYfg7U-LcnC9SIDUW5eohDVSRuAo27xk33GO_a2IOFy-HOBQCLRYlpfT4eG9s1"
        b"hYyBMiF1YeU1uMkMHMflwsX-nz2vp5dvClW496hHpcXJOLbvJ2pCxAqxCbL0HrJU5WRy"
        b"AKu4"
    )

    @override_settings(DEFF_FETCH_URL_NAME="fetch")
    @override_settings(MEDIA_ROOT="/tmp")
    def test_path_starts_media_root(self):
        kwargs = {"path": "/etc/passwd"}
        self.assertEqual(
            self.client.get(reverse("fetch", kwargs=kwargs)).status_code, 404
        )

    @override_settings(DEFF_FETCH_URL_NAME="fetch")
    def test_path_does_not_exist(self):
        kwargs = {"path": "this/file/does/not/exist"}
        self.assertEqual(
            self.client.get(reverse("fetch", kwargs=kwargs)).status_code, 404
        )

    @override_settings(DEFF_FETCH_URL_NAME="fetch")
    @mock.patch("django_encrypted_filefield.views.os.path.exists")
    @mock.patch(
        "django_encrypted_filefield.views.open",
        mock.mock_open(read_data=ENCRYPTED_GIF),
        create=True,
    )
    def test_local_path_exists(self, exists):
        exists.return_value = True
        kwargs = {"path": "dummy-file"}
        response = self.client.get(reverse("fetch", kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.GIF)
        self.assertEqual(response["Content-Type"], "image/gif")
