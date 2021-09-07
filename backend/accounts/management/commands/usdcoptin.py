from django.core.management.base import BaseCommand
from algorand import utils
from django.conf import settings
from algosdk.future.transaction import AssetTransferTxn


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('address', help="Algorand address.", type=str)
        parser.add_argument('private-key', help="Algorand private key.", type=str)

    def handle(self, *args, **options):
        address = options['address']
        private_key = options['private-key']

        txn = AssetTransferTxn(
            address, 
            utils.CLIENT.suggested_params(), 
            address, 
            0, 
            settings.ALGO_ASSET
        )
        stxn = txn.sign(private_key)
        print("Transaction: ", utils.CLIENT.send_transaction(stxn))