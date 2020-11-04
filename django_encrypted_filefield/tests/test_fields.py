from django.db import connection
from django.test import SimpleTestCase

from ..fields import EncryptedFileField, EncryptedImageField


class TestDbType(SimpleTestCase):
    """
    I honestly don't know how to test the remaining bits here.
    """

    def test_db_parameters_respects_db_type_filefield(self):
        f = EncryptedFileField()
        self.assertEqual(f.db_parameters(connection)["type"], "varchar(100)")

    def test_db_parameters_respects_db_type_imagefilefield(self):
        f = EncryptedImageField()
        self.assertEqual(f.db_parameters(connection)["type"], "varchar(100)")
