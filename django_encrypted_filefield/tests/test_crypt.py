from django.test import TestCase

from ..crypt import Cryptographer


class CryptographerTestCase(TestCase):
    """
    I'm not sure how to test this any better.
    """

    def test_encryption(self):
        data = b"This is some data"
        self.assertNotEqual(Cryptographer.encrypted(data), data)

    def test_decryption(self):
        data = b"This is some data"
        self.assertEqual(
            Cryptographer.decrypted(Cryptographer.encrypted(data)),
            data
        )
