import logging
from django.conf import settings
from algosdk.v2client import *
from algosdk import account, util
from algosdk.future.transaction import *
from algosdk.logic import get_application_address
from decimal import *
from collections import defaultdict


logger = logging.getLogger(__name__)

CLIENT = algod.AlgodClient(settings.ALGO_API_TOKEN, settings.ALGO_API_URL)
INDEXER = indexer.IndexerClient(
    indexer_token=settings.ALGO_INDEXER_API_TOKEN,
    indexer_address=settings.ALGO_INDEXER_API_URL
)


def generate_account():
    return account.generate_account()


def check_balance_info(address):
    return CLIENT.account_info(address)


def application_address(app_id):
    return get_application_address(app_id)


def usdc_balance(address):
    getcontext().prec = 6
    info = check_balance_info(address)
    assets = info.get('assets', [])
    for asset in assets:
        if asset.get('asset-id', None) != settings.ALGO_ASSET:
            continue

        return Decimal(asset.get('amount', 0)) / Decimal(1000000)

    return Decimal(0)


def params():
    return CLIENT.suggested_params()


def wait_for_confirmation(transaction_id, timeout=2):
    start_round = CLIENT.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = CLIENT.pending_transaction_info(transaction_id)
        except Exception:
            return False
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(f"Pool error {transaction_id}")
        CLIENT.status_after_block(current_round)
        current_round += 1
    raise Exception(f"Timeout transaction {transaction_id}")


def transfer_algos(sender, receiver, amount, close_remainder_to=None):
    _params = params()
    txn = PaymentTxn(sender.address, _params, receiver.address, int(amount * 1000000),
                     close_remainder_to=close_remainder_to.address if close_remainder_to else None)
    signed_txn = txn.sign(sender.private_key)
    return CLIENT.send_transaction(signed_txn)


def transfer_assets(
    sender, 
    receiver, 
    amount,
    asset=settings.ALGO_ASSET, 
    close_assets_to=None,
    note=None
):
    _params = params()
    atxn = AssetTransferTxn(
        sender.address, 
        _params, 
        receiver.address, 
        util.algos_to_microalgos(amount), 
        asset,
        note=note,
        close_assets_to=close_assets_to.address if close_assets_to else None
    )
    signed_atxn = atxn.sign(sender.private_key)
    return CLIENT.send_transaction(signed_atxn)


def prepare_transfer_algos(
    sender,
    receiver,
    amount,
    close_remainder_to=None
):
    if isinstance(sender, str):
        snd = sender
    else:
        snd = sender.address

    if isinstance(receiver, str):
        rec = receiver
    else:
        rec = receiver.address

    if isinstance(close_remainder_to, str):
        close_remainder_to = close_remainder_to
    elif close_remainder_to is not None:
        close_remainder_to = close_remainder_to.address

    _params = params()
    txn = PaymentTxn(
        snd,
        _params,
        rec,
        util.algos_to_microalgos(amount),
        close_remainder_to=close_remainder_to
    )
    return txn


def prepare_transfer_assets(
    sender,
    receiver,
    amount,
    asset=settings.ALGO_ASSET,
    close_assets_to=None
):
    if isinstance(sender, str):
        snd = sender
    else:
        snd = sender.address

    if isinstance(receiver, str):
        rec = receiver
    else:
        rec = receiver.address

    if isinstance(close_assets_to, str):
        close_assets_to = close_assets_to
    elif close_assets_to is not None:
        close_assets_to = close_assets_to.address

    _params = params()
    atxn = AssetTransferTxn(
        snd,
        _params,
        rec,
        util.algos_to_microalgos(amount),
        asset,
        close_assets_to=close_assets_to
    )
    return atxn


def sign_send_atomic_trasfer(private_keys, txns):
    is_str = isinstance(private_keys, str)
    grouped_txns = assign_group_id(txns)
    signed_txns = list()
    for index, gt in enumerate(grouped_txns):
        signed_txns.append(
            gt.sign(
                private_keys if is_str else private_keys[index]
            )
        )

    return CLIENT.send_transactions(signed_txns)


def get_transactions(**kwargs):
    return INDEXER.search_transactions(
        **kwargs
    )


def get_transactions_info(request_fields=dict(), reply_fields=[]):
    transactions = get_transactions(**request_fields)
    transactions_data = defaultdict(dict)
    for transaction in transactions['transactions']:
        for field in reply_fields:
            if "__" in field:
                ifields = field.split('__')
                data = transaction
                for ifield in ifields:
                    data = data[ifield]
                field = ifield
            else:
                data = transaction[field]
            transactions_data[transaction['sender']][field] = data

    return transactions_data
