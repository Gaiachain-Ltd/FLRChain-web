import logging
import qrcode
import qrcode.image.svg
from django.db import models, transaction
from algorand import utils
from django.conf import settings
from transactions.models import Transaction
from users.models import CustomUser
from algorand.utils import wait_for_confirmation
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

def upload_qr_code(instance, filename):
    return f"accounts/{instance.address}/{filename}"

class Account(models.Model):
    NORMAL_ACCOUNT = 0
    MAIN_ACCOUNT = 1
    PROJECT_ACCOUNT = 2
    ACCOUNT_TYPES = (
        (NORMAL_ACCOUNT, "Normal account"),
        # TODO: Add constraint to keep single main account.
        (MAIN_ACCOUNT, "Main account"),
        (PROJECT_ACCOUNT, "Smart contract account")
    )

    user = models.OneToOneField(
        'users.CustomUser', on_delete=models.SET_NULL,
        null=True, blank=True)
    project = models.OneToOneField(
        'projects.Project', on_delete=models.SET_NULL,
        null=True, blank=True)
    private_key = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=58)
    type = models.PositiveSmallIntegerField(
        default=NORMAL_ACCOUNT, choices=ACCOUNT_TYPES)
    opted_in = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(
        null=True, blank=True, upload_to=upload_qr_code)

    def __str__(self):
        if self.user:
            return f"User: {self.user.name}"
        else:
            return f"Project: {self.project}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.generate_qr_code()

        return super().save(*args, **kwargs)

    @staticmethod
    def get_main_account():
        return Account.objects.get(type=Account.MAIN_ACCOUNT)

    @staticmethod
    def generate(
        entity, 
        account_type=NORMAL_ACCOUNT, 
        initial_amount=settings.ALGO_OPT_IN_AMOUNT, 
        sync=False
    ):
        with transaction.atomic():
            private_key, address = utils.generate_account()
            logger.debug("Generated algorand account for %s.", entity)

            created_account = Account.objects.create(
                private_key=private_key,
                address=address,
                type=account_type,
                **{'user': entity} if account_type != Account.PROJECT_ACCOUNT else {'project': entity}
            )
            logger.debug("Created account for %s.", entity)

            # ONLY FOR TEST PURPOSES!!
            if account_type == Account.NORMAL_ACCOUNT and entity.type == CustomUser.INVESTOR and (settings.TESTING or settings.AUTO_INV_FUELING == '1'):
                main_account = Account.get_main_account()
                chained = [
                    Transaction.prepare_transfer(
                        main_account,
                        created_account,
                        0.01,
                        action=Transaction.FUELING),
                    Transaction.prepare_transfer(
                        main_account,
                        created_account,
                        1,
                        currency=Transaction.USDC,
                        action=Transaction.FUELING)]
            else:
                chained = []

            tx_ids = created_account.opt_in(chained, initial_amount=initial_amount)
            if sync:
                for tx_id in tx_ids:
                    wait_for_confirmation(tx_id)

            return created_account

    def opt_in(self, chain=[], initial_amount=settings.ALGO_OPT_IN_AMOUNT):
        main_account = Account.get_main_account()
        logger.debug("Opt-In transaction for %s account.", self.address)
        return Transaction.opt_in(
            self,
            main_account,
            chain,
            initial_amount=initial_amount
        )

    def generate_qr_code(self):
        img = qrcode.make(f"algorand://{self.address}", version=1, image_factory=qrcode.image.svg.SvgPathImage)
        cp = ContentFile(b'')
        img.save(cp)
        self.qr_code.save('qr_code.svg', cp, save=False)

    def usdc_balance(self):
        return utils.usdc_balance(self.address)
