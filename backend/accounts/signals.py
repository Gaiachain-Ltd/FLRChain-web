from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from users.models import CustomUser
from accounts.models import Account
from django.db import transaction
from algorand import utils


def on_user_post_save_impl(user):
     Account.generate(user)

def on_account_pre_delete_impl(account):
    main = Account.get_main_account()
    txid = utils.transfer_algos(
        account.address,
        account.private_key,
        main.address,
        0,
        main.address)
    utils.wait_for_confirmation(txid)


@receiver(post_save, sender=CustomUser)
def on_user_post_save(sender, instance, created, **kwargs):
    if not created or instance.type == CustomUser.ADMINISTRATOR:
        return

    if not transaction.get_connection().in_atomic_block:
        on_user_post_save_impl(instance)
    else:
        transaction.on_commit(lambda: on_user_post_save_impl(instance))

@receiver(pre_delete, sender=Account)
def on_account_pre_delete(sender, instance, **kwargs):
    if not transaction.get_connection().in_atomic_block:
        on_account_pre_delete_impl(instance)
    else:
        transaction.on_commit(lambda: on_account_pre_delete_impl(instance))