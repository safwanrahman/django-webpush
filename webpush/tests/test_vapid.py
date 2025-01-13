import unittest

from cryptography.hazmat.primitives import serialization
from py_vapid import Vapid, b64urlencode
from webpush.vapid import get_vapid_keypair


class TestGetVapidKeypair(unittest.TestCase):
    def test_keypair_is_consistent(self):
        # GIVEN a generated pair of public key and private key
        pubkey, privkey = get_vapid_keypair()

        # WHEN instantiating a new Vapid keypair from the private key
        newkey = Vapid.from_raw(privkey.encode())

        # THEN the public key export is the same as the one generated
        self.assertEqual(
            b64urlencode(
                newkey.public_key.public_bytes(
                    serialization.Encoding.X962,
                    serialization.PublicFormat.UncompressedPoint,
                )
            ),
            pubkey,
        )
