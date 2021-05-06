import logging
import datetime
from celery import shared_task
from transactions.models import Transaction
from algorand import utils


logger = logging.getLogger(__name__)


@shared_task()
def verify_transactions():
    pending_transactions = Transaction.objects.filter(
        status=Transaction.PENDING)

    for pending_transaction in pending_transactions:
        status = utils.status()
        info = utils.transaction_info(pending_transaction.txid)
        
        confirmed_round = info.get("confirmed-round", 0)
        if confirmed_round > 0 and confirmed_round <= status['last-round']:
            pending_transaction.status = Transaction.CONFIRMED
            pending_transaction.save()
        elif info['pool-error'] or info['txn']['txn']['lv'] < status['last-round']:
            pending_transaction.status = Transaction.REJECTED
            pending_transaction.save()

            try:
                pending_transaction.retry()
            except Exception as e:
                logger.error(e)
