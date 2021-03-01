from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import CustomUser
from accounts.models import Account
from django.db import transaction


def on_user_post_save_impl(user):
     Account.generate(user)

@receiver(post_save, sender=CustomUser)
def on_user_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    if not transaction.get_connection().in_atomic_block:
        on_user_post_save_impl(instance)
    else:
        transaction.on_commit(lambda: on_user_post_save_impl(instance))