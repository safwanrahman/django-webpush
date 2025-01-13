from cryptography.hazmat.primitives import serialization
from py_vapid import Vapid
from py_vapid.utils import num_to_bytes, b64urlencode


def get_vapid_keypair() -> tuple[str, str]:
    vapid = Vapid()
    vapid.generate_keys()

    pubkey_export = vapid.public_key.public_bytes(
        serialization.Encoding.X962,
        serialization.PublicFormat.UncompressedPoint,
    )
    privkey_export = num_to_bytes(vapid.private_key.private_numbers().private_value, 32)

    return b64urlencode(pubkey_export), b64urlencode(privkey_export)
