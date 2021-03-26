import logging
import base64
import datetime
import accounts
from django.conf import settings
from algosdk.v2client import *
from algosdk import account
from algosdk.future.transaction import PaymentTxn, AssetTransferTxn, calculate_group_id
from decimal import *


logger = logging.getLogger(__name__)

CLIENT = algod.AlgodClient(settings.ALGO_API_TOKEN, settings.ALGO_API_URL)


def generate_account():
    return account.generate_account()


def check_balance_info(address):
    return CLIENT.account_info(address)


def usdc_balance(address):
    getcontext().prec = 6
    info = check_balance_info(address)
    assets = info.get('assets', [])
    for asset in assets:
        if asset.get('asset-id', None) != settings.ALGO_ASSET:
            continue

        return Decimal(asset.get('amount', 0)) / Decimal(1000000)

    return Decimal(0)


def algo_balance(address):
    info = check_balance_info(address)
    return Decimal(info.get('amount', 0) / 1000000)


def params():
    return CLIENT.suggested_params()


def compile(source):
    return CLIENT.compile(source)


def date_time_to_blocks(date_time):
    _params = params()
    now = datetime.datetime.now()
    diff = (date_time - now.date()).seconds
    return _params.first + int(diff / 4.5)


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


def transfer_algos(sender, receiver, amount, close_remainder_to=None):
    params = CLIENT.suggested_params()
    txn = PaymentTxn(sender.address, params, receiver.address, int(amount * 1000000),
                     close_remainder_to=close_remainder_to.address if close_remainder_to else None)
    if sender.type == accounts.models.Account.SMART_CONTRACT_ACCOUNT:
        signed_txn = sender.smart_contract.sign(txn)
    else:
        signed_txn = txn.sign(sender.private_key)
    fee = (params.min_fee if params.fee == 0 else params.fee) / 1000000
    return CLIENT.send_transaction(signed_txn), fee


def transfer_assets(sender, receiver, amount, 
                    asset=settings.ALGO_ASSET, close_assets_to=None):
    params = CLIENT.suggested_params()
    atxn = AssetTransferTxn(sender.address, params, receiver.address, int(amount * 1000000), asset, 
                            close_assets_to=close_assets_to.address if close_assets_to else None)
    if sender.type == accounts.models.Account.SMART_CONTRACT_ACCOUNT:
        signed_atxn = sender.smart_contract.sign(atxn)
    else:
        signed_atxn = atxn.sign(sender.private_key)
    fee = (params.min_fee if params.fee == 0 else params.fee) / 1000000
    return CLIENT.send_transaction(signed_atxn), fee


def prepare_transfer_algos(sender, receiver, amount, 
                          close_remainder_to=None):
    params = CLIENT.suggested_params()
    txn = PaymentTxn(sender.address, params, receiver.address, int(amount * 1000000),
                     close_remainder_to=close_remainder_to.address if close_remainder_to else None)
    fee = (params.min_fee if params.fee == 0 else params.fee) / 1000000
    return txn, fee


def prepare_transfer_assets(sender, receiver, amount, 
                    asset=settings.ALGO_ASSET, close_assets_to=None):
    params = CLIENT.suggested_params()
    atxn = AssetTransferTxn(sender.address, params, receiver.address, int(amount * 1000000), asset, 
                            close_assets_to=close_assets_to.address if close_assets_to else None)
    fee = (params.min_fee if params.fee == 0 else params.fee) / 1000000
    return atxn, fee


def atomic_transfer(txns):
    gtxn = calculate_group_id([txn[0] for txn in txns])

    sgtxns = list()
    for txn in txns:
        txn[0].group = gtxn
        
        if txn[1].from_account.type == accounts.models.Account.SMART_CONTRACT_ACCOUNT:
            signed = txn[1].from_account.smart_contract.sign(txn[0])
            sgtxns.append(signed)
        else:
            signed = txn[0].sign(txn[1].from_account.private_key)
            sgtxns.append(signed)

        txn[1].txid = signed.get_txid()

    CLIENT.send_transactions(sgtxns)
    return base64.b64encode(gtxn).decode('ascii')