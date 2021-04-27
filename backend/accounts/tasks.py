import logging
from celery import shared_task
from accounts.models import Account
from transactions.models import Transaction


logger = logging.getLogger(__name__)


@shared_task()
def transfer_back_funds():
    accounts = Account.objects.filter(
        user__isnull=True,
        smart_contract__isnull=True,
        type=Account.NORMAL_ACCOUNT)[:10]

    try:
        main = Account.get_main_account()
    except Exception as e:
        logger.error("Error: %s", e)
        return
        
    for account in accounts:
        try:
            Transaction.transfer(
                account,
                main,
                0,
                Transaction.USDC,
                Transaction.CLOSE,
                main)
            Transaction.transfer(
                account,
                main,
                0,
                Transaction.ALGO,
                Transaction.CLOSE,
                main)

            account.delete()
            logger.warning("Account %s closed.", account.address)
        except Exception as e:
            logger.error("Error: %s", e)