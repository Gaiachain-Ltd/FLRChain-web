import logging
import base64
from django.conf import settings
from algosdk.v2client import *
from algosdk import account
from algosdk.future.transaction import PaymentTxn, AssetTransferTxn, calculate_group_id


logger = logging.getLogger(__name__)

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
        logger.debug("Waiting for confirmation")
        last_round += 1
        CLIENT.status_after_block(last_round)
        txinfo = CLIENT.pending_transaction_info(txid)
    logger.debug("Transaction {} confirmed in round {}.".format(
        txid, txinfo.get('confirmed-round')))
    return txinfo

def transfer_algos(sender, sender_pk, receiver, amount, close_remainder_to=None):
    params = CLIENT.suggested_params()
    txn = PaymentTxn(sender, params, receiver, amount,
                     close_remainder_to=close_remainder_to)
    signed_txn = txn.sign(sender_pk)
    return CLIENT.send_transaction(signed_txn), params.min_fee if params.fee == 0 else params.fee


def transfer_assets(sender, sender_pk, receiver, amount, 
                    asset=settings.ALGO_ASSET, close_assets_to=None):
    params = CLIENT.suggested_params()
    atxn = AssetTransferTxn(sender, params, receiver, amount, asset, 
                            close_assets_to=close_assets_to)
    signed_atxn = atxn.sign(sender_pk)
    return CLIENT.send_transaction(signed_atxn), params.min_fee if params.fee == 0 else params.fee


def prepare_transfer_algos(sender, sender_pk, receiver, amount, 
                          close_remainder_to=None):
    params = CLIENT.suggested_params()
    txn = PaymentTxn(sender, params, receiver, amount,
                     close_remainder_to=close_remainder_to)
    return txn, params.min_fee if params.fee == 0 else params.fee


def prepare_transfer_assets(sender, sender_pk, receiver, amount, 
                    asset=settings.ALGO_ASSET, close_assets_to=None):
    params = CLIENT.suggested_params()
    atxn = AssetTransferTxn(sender, params, receiver, amount, asset, 
                            close_assets_to=close_assets_to)
    return atxn, params.min_fee if params.fee == 0 else params.fee


def atomic_transfer(txns):
    gtxn = calculate_group_id([txn[0] for txn in txns])

    sgtxns = list()
    for txn in txns:
        txn[0].group = gtxn
        sgtxns.append(txn[0].sign(txn[1].from_user.account.private_key))

    CLIENT.send_transactions(sgtxns)
    return base64.b64encode(gtxn).decode('ascii')