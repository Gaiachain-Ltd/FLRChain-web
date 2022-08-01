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


def reserved_algos(address):
    info = check_balance_info(address)

    opted_in_apps_cost = 0
    if info.get("total-apps-opted-in", None) is not None:
        opted_in_apps_cost = info["total-apps-opted-in"] * 100000

    opted_in_assets_cost = 0
    if info.get("total-assets-opted-in", None) is not None:
        opted_in_assets_cost = info["total-assets-opted-in"] * 100000

    apps_created_cost = 0
    if info.get("total-created-apps", None) is not None:
        apps_created_cost = info["total-created-apps"] * 100000

    assets_created_cost = 0
    if info.get("total-created-assets", None) is not None:
        assets_created_cost = info["total-created-assets"] * 100000

    apps_uint_cost = 0
    apps_byte_slice_cost = 0
    if info.get("apps-total-schema", None) is not None and (opted_in_apps_cost > 0 or apps_created_cost > 0):
        apps_uint_cost = info["apps-total-schema"]["num-uint"] * 28500
        apps_byte_slice_cost = info["apps-total-schema"]["num-byte-slice"] * 50000

    apps_extra_pages_cost = 0
    if info.get("apps-total-extra-pages", None) is not None:
        apps_extra_pages_cost = info["apps-total-extra-pages"] * 100000

    return (
        opted_in_apps_cost + 
        opted_in_assets_cost + 
        apps_created_cost + 
        assets_created_cost + 
        apps_uint_cost + 
        apps_byte_slice_cost + 
        apps_extra_pages_cost
    ), info["amount"]

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
        note=note,
        close_assets_to=close_assets_to
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
