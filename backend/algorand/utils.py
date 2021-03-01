from django.conf import settings
from algosdk.v2client import *
from algosdk import account
from algosdk.future.transaction import PaymentTxn

CLIENT = algod.AlgodClient(settings.ALGO_API_TOKEN, settings.ALGO_API_URL)

def generate_account():
    return account.generate_account()

def check_balance(address):
    return CLIENT.account_info(address)['amount']

def wait_for_confirmation(txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = CLIENT.status().get('last-round')
    txinfo = CLIENT.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        CLIENT.status_after_block(last_round)
        txinfo = CLIENT.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

def transfer_algos(sender, sender_pk, receiver, amount, close_remainder_to=None):
    params = CLIENT.suggested_params()
    txn = PaymentTxn(sender, params, receiver, amount, close_remainder_to=close_remainder_to)
    signed_txn = txn.sign(sender_pk)
    return CLIENT.send_transaction(signed_txn)