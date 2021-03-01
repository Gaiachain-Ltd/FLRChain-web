from django.db import models, transaction
from algosdk import account, encoding, algod, transaction as algo_transaction
from django.conf import settings


client = algod.AlgodClient(settings.ALGO_API_TOKEN, settings.ALGO_API_URL)


class Account(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    private_key = models.CharField(max_length=128)
    address = models.CharField(max_length=58)

    @staticmethod
    def generate(user):
        with transaction.atomic():
            private_key, address = account.generate_account()

            if not encoding.is_valid_address(address):
                raise Exception("Generated account address is not valid!", address, user)

            created_account = Account.objects.create(
                user=user,
                private_key=private_key,
                address=address)
            return created_account

    def balance(self):
        return client.account_info(self.address)['amount']

    def transfer(self, amount, receiver):

        if isinstance(receiver, Account):
            receiver = receiver.address

        params = client.suggested_params()
        gen_hash = params["genesishashb64"]
        first_valid_round = params["lastRound"]
        last_valid_round = first_valid_round + 1000
        fee = params["fee"]

        tx = algo_transaction.PaymentTxn(
            self.address, 
            fee, 
            first_valid_round, 
            last_valid_round, 
            gen_hash, 
            receiver, 
            amount)

        signed_tx = tx.sign(self.private_key)
        
        tx_confirm = client.send_transaction(signed_tx)

        client.status_after_block(first_valid_round + 2)

        return tx_confirm