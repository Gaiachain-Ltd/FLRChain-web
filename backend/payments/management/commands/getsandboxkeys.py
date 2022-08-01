from django.conf import settings
from django.core.management.base import BaseCommand
from payments.mtn import MTNAPI


class Command(BaseCommand):
    def handle(self, *args, **options):
        mtn_client = MTNAPI(
            settings.MTN_SUBSCRIPTION_KEY,
            url="https://sandbox.momodeveloper.mtn.com",
            callback=settings.MTN_CALLBACK_HOST,
        )

        reply = mtn_client.sandbox_user()
        if reply.status_code != 201:
            print(f"Cannot create API user, code {reply.status_code}")
            return

        reply = mtn_client.sandbox_keys()
        if reply.status_code != 201:
            print(f"Cannot create API keys, code {reply.status_code}")
            return

        print(mtn_client.USER_ID, mtn_client.API_KEY)

        