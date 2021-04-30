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


def wait_for_confirmation(transaction_id, timeout=1000):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = CLIENT.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = CLIENT.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"])) 
        CLIENT.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))


def transfer_algos(sender, receiver, amount, close_remainder_to=None):
    _params = params()
    txn = PaymentTxn(sender.address, _params, receiver.address, int(amount * 1000000),
                     close_remainder_to=close_remainder_to.address if close_remainder_to else None)
    if sender.type == accounts.models.Account.SMART_CONTRACT_ACCOUNT:
        signed_txn = sender.smart_contract.sign(txn)
    else:
        signed_txn = txn.sign(sender.private_key)
    fee = (_params.min_fee if _params.fee == 0 else _params.fee) / 1000000
    return CLIENT.send_transaction(signed_txn), fee


def transfer_assets(sender, receiver, amount, 
                    asset=settings.ALGO_ASSET, close_assets_to=None):
    _params = params()
    atxn = AssetTransferTxn(sender.address, _params, receiver.address, int(amount * 1000000), asset, 
                            close_assets_to=close_assets_to.address if close_assets_to else None)
    if sender.type == accounts.models.Account.SMART_CONTRACT_ACCOUNT:
        signed_atxn = sender.smart_contract.sign(atxn)
    else:
        signed_atxn = atxn.sign(sender.private_key)
    fee = (_params.min_fee if _params.fee == 0 else _params.fee) / 1000000
    return CLIENT.send_transaction(signed_atxn), fee


def prepare_transfer_algos(sender, receiver, amount, 
                          close_remainder_to=None):
    _params = params()
    txn = PaymentTxn(sender.address, _params, receiver.address, int(amount * 1000000),
                     close_remainder_to=close_remainder_to.address if close_remainder_to else None)
    fee = (_params.min_fee if _params.fee == 0 else _params.fee) / 1000000
    return txn, fee


def prepare_transfer_assets(sender, receiver, amount, 
                    asset=settings.ALGO_ASSET, close_assets_to=None):
    _params = params()
    atxn = AssetTransferTxn(sender.address, _params, receiver.address, int(amount * 1000000), asset, 
                            close_assets_to=close_assets_to.address if close_assets_to else None)
    fee = (_params.min_fee if _params.fee == 0 else _params.fee) / 1000000
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