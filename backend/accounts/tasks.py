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

    main = Account.get_main_account()
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
            logging.warning("Account %s closed.", account.address)
        except Exception as e:
            logging.error("Error: %s", e)