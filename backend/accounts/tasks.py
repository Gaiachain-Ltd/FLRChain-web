import logging
from celery import shared_task
from accounts.models import Account
from algorand.utils import CLIENT, wait_for_confirmation, sign_send_atomic_trasfer, prepare_transfer_algos, prepare_transfer_assets
from django.conf import settings


logger = logging.getLogger(__name__)


@shared_task()
def opt_in_accounts():
    accounts = Account.objects.filter(
        type=Account.NORMAL_ACCOUNT,
        opted_in=False
    )[:1]
    
    for account in accounts:
        info = CLIENT.account_info(account.address)
        for asset in info.get("assets", []):
            if asset.get("asset-id", None) == settings.ALGO_ASSET:
                account.opted_in = True
                account.save()
                break
        
        if not accounts.opted_in:
            main_account = Account.get_main_account()
            txn1 = prepare_transfer_algos(
                main_account.address, 
                account.address,
                settings.ALGO_OPT_IN_AMOUNT
            )
            txn2 = prepare_transfer_assets(
                account.address,
                account.address,
                0
            )
            txn = sign_send_atomic_trasfer(
                [main_account.private_key, account.private_key],
                [txn1, txn2]
            )
            wait_for_confirmation(txn)

            account.opted_in = True
            account.save()


@shared_task()
def transfer_back_funds():
    accounts = Account.objects.filter(
        user__isnull=True,
        type=Account.NORMAL_ACCOUNT)[:10]

    try:
        main = Account.get_main_account()
    except Exception as e:
        logger.error("Error: %s", e)
        return
        
    for account in accounts:
        try:
            prepare_transfer_assets(
                account,
                main,
                0.0,
                close_assets_to=main
            )
            prepare_transfer_algos(
                account,
                main,
                0.0,
                close_remainder_to=main
            )
            account.delete()
            logger.warning("Account %s closed.", account.address)
        except Exception as e:
            logger.error("Error: %s", e)