from django.core.management.base import BaseCommand

from ...vapid import get_vapid_keypair


class GenerateValidKeys(BaseCommand):
    def handle(self, *args, **options):
        pubkey, privkey = get_vapid_keypair()
        self.stdout.write(f"Public key: {pubkey}")
        self.stdout.write(f"Private key: {privkey}")
