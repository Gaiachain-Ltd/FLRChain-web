import secrets
import base64
import logging
from decimal import *
from django.db import models
from pyteal import *
from accounts.models import Account
from algorand import utils
from django.conf import settings
from algosdk.future.transaction import LogicSig, LogicSigTransaction
from django.db import transaction
from algosdk import logic
from transactions.models import Transaction


logger = logging.getLogger(__name__)


def default_secret():
    return secrets.token_hex(16)


class SmartContract(models.Model):
    investment = models.OneToOneField(
        'investments.Investment', on_delete=models.CASCADE)
    project = models.OneToOneField(
        'projects.Project', on_delete=models.CASCADE)
    secret = models.CharField(max_length=32, default=default_secret)
    program = models.TextField(blank=True, null=True)

    @staticmethod
    def generate(investment):
        with transaction.atomic():
            smart_contract = SmartContract.objects.create(
                investment=investment,
                project=investment.project)

            smart_contract_address = smart_contract.compile()

            smart_contract_account = Account.objects.create(
                smart_contract=smart_contract,
                address=smart_contract_address,
                type=Account.SMART_CONTRACT_ACCOUNT)

            getcontext().prec = 6
            facilitator_fee = investment.amount * Decimal(settings.FACILITATOR_FEE)
            investment_amount = investment.amount - facilitator_fee
            
            return (smart_contract_account.opt_in([
                Transaction.prepare_transfer(
                    investment.investor.account,
                    investment.project.owner.account,
                    facilitator_fee,
                    currency=Transaction.USDC,
                    action=Transaction.FACILITATOR_FEE,
                    project=investment.project
                ),
                Transaction.prepare_transfer(
                    investment.investor.account,
                    smart_contract_account,
                    investment_amount,
                    currency=Transaction.USDC,
                    action=Transaction.INVESTMENT,
                    project=investment.project)
            ]), smart_contract_account)
        
    def compile(self):
        def _logic(secret, facililator_address, investor_address, deadline):
            is_beneficiary_reward = And(
                Ed25519Verify(Bytes(secret), Arg(0), Addr(facililator_address)), #Check secret
                # Txn.first_valid() < Int(deadline), # Reward could be claimed only if deadline hasn't been met
                Txn.type_enum() == TxnType.AssetTransfer, # Rewards only in asset (USDC)
                Txn.xfer_asset() == Int(settings.ALGO_ASSET), # USDC
                Txn.asset_close_to() == Global.zero_address(),
                Txn.rekey_to() == Global.zero_address())
            
            is_investor_transfer_back = And(
                Txn.rekey_to() == Global.zero_address(),
                Txn.first_valid() >= Int(deadline), # Investor can transfer back after deadline
                Or(And(Txn.close_remainder_to() == Addr(investor_address),
                    Txn.receiver() == Addr(investor_address)),
                And(Txn.asset_close_to() == Addr(investor_address),
                    Txn.asset_receiver() == Addr(investor_address))))
            
            is_opt_in = And(Txn.type_enum() == TxnType.AssetTransfer,
                            Txn.xfer_asset() == Int(settings.ALGO_ASSET),
                            Txn.asset_amount() == Int(0),
                            Txn.asset_close_to() == Global.zero_address(),
                            Txn.rekey_to() == Global.zero_address(),
                            Txn.close_remainder_to() == Global.zero_address())
            
            return Or(is_beneficiary_reward, is_investor_transfer_back, is_opt_in)
        
        source_teal = compileTeal(
            _logic(
                self.secret,
                self.project.owner.account.address,
                self.investment.investor.account.address,
                utils.date_time_to_blocks(self.investment.end)),
            Mode.Signature)

        compile_reply = utils.compile(source_teal)
        self.program = compile_reply['result']
        self.save()
        
        return LogicSig(base64.decodebytes(self.program.encode())).address()

    def sign(self, transaction):
        decoded_program = base64.decodebytes(self.program.encode())
        arg1 = logic.teal_sign_from_program(
            self.project.owner.account.private_key, 
            self.secret.encode(), 
            decoded_program)

        lsig = LogicSig(decoded_program, args=[arg1])
        return LogicSigTransaction(transaction, lsig)

    def check_if_sufficient_balance(self, amount=None, extra=0):
        balance = self.account.usdc_balance()

        if amount:
            return amount <= balance
        else:
            for reward in [task.reward for task in self.project.tasks.filter(deleted=False)]:
                print("REW/BAL", reward, balance)
                if reward + extra <= balance:
                    return True

            return False