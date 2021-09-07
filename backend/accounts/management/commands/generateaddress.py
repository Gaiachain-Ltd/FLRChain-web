from django.core.management.base import BaseCommand
from algorand import utils


class Command(BaseCommand):
    def handle(self, *args, **options):
        private_key, address = utils.generate_account()
        print("Address: ", address)
        print("Private key: ", private_key)
