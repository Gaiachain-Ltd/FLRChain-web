import base64
import datetime
from collections import defaultdict
from algosdk.v2client import *
from algosdk.future import *
from algosdk.logic import *
from pyteal import *
from algorand.utils import (INDEXER, CLIENT, wait_for_confirmation, prepare_transfer_algos,
                            prepare_transfer_assets, sign_send_atomic_trasfer)
from django.conf import settings


def approval_program():
    G_STATUS_KEY = Bytes("status")
    G_TOTAL_KEY = Bytes("total")
    G_COUNT_KEY = Bytes("count")
    G_START_KEY = Bytes("start")
    G_END_KEY = Bytes("end")
    G_ADM_KEY = Bytes("adm")

    L_TOTAL_KEY = Bytes("total")
    L_ROLE_KEY = Bytes("role")
    L_JOIN_KEY = Bytes("join")
    L_COUNT_KEY = Bytes("count")
    L_BALANCE_KEY = Bytes("balance")

    INITIAL_STATUS = Int(0)
    INITIALIZED_STATUS = Int(1)
    STARTED_STATUS = Int(2)
    FINISHED_STATUS = Int(3)

    FACILILTATOR_ROLE = Int(1)
    INVESTOR_ROLE = Int(2)
    BENEFICIARY_ROLE = Int(3)

    ACCEPTED_JOIN = Int(1)
    REJECTED_JOIN = Int(2)

    ACCEPTED_VERIFY = Int(1)
    REJECTED_VERIFY = Int(2)

    is_initialized = App.globalGet(G_STATUS_KEY) == INITIALIZED_STATUS

    is_started = App.globalGet(G_STATUS_KEY) == STARTED_STATUS

    is_creator = Global.creator_address() == Txn.sender()

    is_facilitator = App.localGet(
        Txn.sender(), L_ROLE_KEY) == FACILILTATOR_ROLE

    is_opted_in = App.localGet(Txn.sender(), L_ROLE_KEY) != Int(0)

    is_beneficiary = App.localGet(Txn.sender(), L_ROLE_KEY) == BENEFICIARY_ROLE

    is_investor = App.localGet(Txn.sender(), L_ROLE_KEY) == INVESTOR_ROLE

    @Subroutine(TealType.uint64)
    def is_accepted(account):
        return App.localGet(account, L_JOIN_KEY) == ACCEPTED_JOIN

    @Subroutine(TealType.none)
    def set_project_properties():
        return Seq([
            Assert(
                And(
                    Btoi(Txn.application_args[1]) < Btoi(
                        Txn.application_args[2]),
                    Btoi(Txn.application_args[2]) > Global.latest_timestamp()
                )
            ),
            App.globalPut(G_START_KEY, Btoi(Txn.application_args[1])),
            App.globalPut(G_END_KEY, Btoi(Txn.application_args[2])),
            App.globalPut(G_ADM_KEY, Btoi(Txn.application_args[3])),
        ])

    @Subroutine(TealType.uint64)
    def facilitator_adm_fee_withdraw():
        return Minus(
            App.globalGet(G_ADM_KEY),
            App.localGet(Txn.sender(), L_TOTAL_KEY)
        )

    @Subroutine(TealType.uint64)
    def investor_withdraw(project_balance):
        return Mul(
            Div(
                App.localGet(Txn.sender(), L_TOTAL_KEY),
                Minus(
                    App.globalGet(G_TOTAL_KEY),
                    App.globalGet(G_ADM_KEY)
                )
            ),
            project_balance
        )

    on_init = Seq([
        Assert(Not(is_initialized)),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.xfer_asset: Txn.assets[0],
            TxnField.asset_receiver: Global.current_application_address(),
            TxnField.asset_amount: Int(0),
        }),
        InnerTxnBuilder.Submit(),
        App.globalPut(G_STATUS_KEY, INITIALIZED_STATUS),
        Approve()
    ])

    on_invest = Seq([
        Assert(Or(is_initialized, is_started)),
        Assert(is_investor),
        Assert(
            And(
                Global.group_size() == Int(3),
                Gtxn[2].type_enum() == TxnType.AssetTransfer,
                Gtxn[2].xfer_asset() == Txn.assets[0],
                Gtxn[2].asset_receiver() == Global.current_application_address()
            )
        ),
        If(App.localGet(Txn.sender(), L_TOTAL_KEY) == Int(0)).
        Then(
            App.globalPut(
                G_COUNT_KEY,
                Add(
                    App.globalGet(G_COUNT_KEY),
                    Int(1)
                )
            )
        ),
        App.localPut(
            Txn.sender(),
            L_TOTAL_KEY,
            Add(
                App.localGet(Txn.sender(), L_TOTAL_KEY),
                Gtxn[2].asset_amount()
            )
        ),
        App.globalPut(
            G_TOTAL_KEY,
            Add(
                App.globalGet(G_TOTAL_KEY),
                Gtxn[2].asset_amount()
            )
        ),
        Approve()
    ])

    on_join = Seq([
        Assert(Or(is_initialized, is_started)),
        Assert(is_facilitator),
        Assert(
            Or(
                Btoi(Txn.application_args[1]) == ACCEPTED_JOIN,
                Btoi(Txn.application_args[1]) == REJECTED_JOIN
            )
        ),
        App.localPut(Txn.accounts[1], L_JOIN_KEY,
                     Btoi(Txn.application_args[1])),
        Approve()
    ])

    on_work = Seq([
        Assert(Or(is_initialized, is_started)),
        Assert(is_beneficiary),
        Assert(is_accepted(Txn.sender())),
        App.localPut(
            Txn.sender(),
            L_TOTAL_KEY,
            Add(
                App.localGet(Txn.sender(), L_TOTAL_KEY),
                Btoi(Txn.application_args[1])
            )
        ),
        App.localPut(
            Txn.sender(),
            L_COUNT_KEY,
            Add(
                App.localGet(Txn.sender(), L_COUNT_KEY),
                Int(1)
            )
        ),
        Approve()
    ])

    # TODO: Checks
    on_verify = Seq([
        Assert(Or(is_initialized, is_started)),
        Assert(is_accepted(Txn.accounts[1])),
        Assert(
            Or(
                Btoi(Txn.application_args[2]) == ACCEPTED_VERIFY,
                Btoi(Txn.application_args[2]) == REJECTED_VERIFY
            )
        ),
        App.localPut(
            Txn.accounts[1],
            L_TOTAL_KEY,
            Minus(
                App.localGet(Txn.accounts[1], L_TOTAL_KEY),
                Btoi(Txn.application_args[1])
            )
        ),
        App.localPut(
            Txn.accounts[1],
            L_COUNT_KEY,
            Minus(
                App.localGet(Txn.accounts[1], L_COUNT_KEY),
                Int(1)
            )
        ),
        If(Btoi(Txn.application_args[2]) == ACCEPTED_VERIFY).
        Then(
            Seq([
                App.localPut(
                    Txn.accounts[1],
                    L_BALANCE_KEY,
                    Add(
                        App.localGet(Txn.accounts[1], L_BALANCE_KEY),
                        Btoi(Txn.application_args[1])
                    )
                ),
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: Txn.assets[0],
                    TxnField.asset_receiver: Txn.accounts[1],
                    TxnField.asset_amount: Btoi(Txn.application_args[1]),
                }),
                InnerTxnBuilder.Submit(),
            ])
        ),
        Approve()
    ])

    app_balance = AssetHolding.balance(
        Global.current_application_address(),
        Txn.assets[0]
    )

    on_withdraw = Seq([
        Assert(
            Or(
                is_facilitator,
                is_investor
            )
        ),
        app_balance,
        If(is_facilitator).
        Then(
            Seq([
                Approve(),
                # Assert(facilitator_adm_fee_withdraw() > Int(0)),
                # InnerTxnBuilder.Begin(),
                # InnerTxnBuilder.SetFields({
                #     TxnField.type_enum: TxnType.AssetTransfer,
                #     TxnField.xfer_asset: Txn.assets[0],
                #     TxnField.asset_receiver: Txn.sender(),
                #     TxnField.asset_amount: facilitator_adm_fee_withdraw()
                # }),
                # InnerTxnBuilder.Submit(),
                # App.localPut(Txn.sender(), L_TOTAL_KEY, Add(
                #     App.localGet(Txn.sender(), L_TOTAL_KEY),
                #     facilitator_adm_fee_withdraw()
                # ))
            ])
        ).
        ElseIf(is_investor).
        Then(
            Seq([
                Assert(App.localGet(Txn.sender(), L_COUNT_KEY) == Int(0)),
                Assert(investor_withdraw(app_balance.value()) > Int(0)),
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: Txn.assets[0],
                    TxnField.asset_receiver: Txn.sender(),
                    TxnField.asset_amount: investor_withdraw(app_balance.value()),
                }),
                InnerTxnBuilder.Submit(),
                App.localPut(Txn.sender(), L_COUNT_KEY, Int(1))
            ])
        ).
        Else(Reject()),
        Approve()
    ])

    on_start = Seq([
        Assert(is_initialized),
        Assert(is_facilitator),
        App.globalPut(G_STATUS_KEY, STARTED_STATUS),
        set_project_properties(),
        Approve()
    ])

    on_update = Seq([
        Assert(is_started),
        Assert(is_facilitator),
        set_project_properties(),
        App.globalPut(G_STATUS_KEY, Txn.application_args[4]),
        Approve()
    ])

    on_batch = Seq([
        Assert(is_started),
        Assert(is_facilitator),
        Assert(App.localGet(Txn.accounts[1], L_ROLE_KEY) == BENEFICIARY_ROLE),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.xfer_asset: Txn.assets[0],
            TxnField.asset_receiver: Txn.accounts[1],
            TxnField.asset_amount: Btoi(Txn.application_args[2]),
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    ])

    handle_noop = Cond(
        [Txn.application_args[0] == Bytes("INIT"), on_init],
        [Txn.application_args[0] == Bytes("INVEST"), on_invest],
        [Txn.application_args[0] == Bytes("JOIN"), on_join],
        [Txn.application_args[0] == Bytes("WORK"), on_work],
        [Txn.application_args[0] == Bytes("VERIFY"), on_verify],
        [Txn.application_args[0] == Bytes("WITHDRAW"), on_withdraw],
        [Txn.application_args[0] == Bytes("START"), on_start],
        [Txn.application_args[0] == Bytes("UPDATE"), on_update],
        [Txn.application_args[0] == Bytes("BATCH"), on_batch],
    )

    handle_delete = Seq([
        Assert(is_creator),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.xfer_asset: Txn.assets[0],
            TxnField.asset_amount: Int(0),
            TxnField.asset_receiver: Txn.sender(),
            TxnField.asset_close_to: Txn.sender(),
        }),
        InnerTxnBuilder.Submit(),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.amount: Int(0),
            TxnField.receiver: Txn.sender(),
            TxnField.close_remainder_to: Txn.sender(),
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    ])

    handle_update = Seq([
        Assert(is_creator),
        Approve()
    ])

    handle_optin = Seq([
        Assert(Or(is_initialized, is_started)),
        Assert(Not(is_opted_in)),
        App.localPut(Txn.sender(), L_ROLE_KEY, Btoi(Txn.application_args[0])),
        Approve()
    ])

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, Approve()],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )
    return compileTeal(program, Mode.Application, version=5)


def clear_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=5)


def create(creator_address, creator_pk):
    approval_compiled = CLIENT.compile(approval_program())
    clear_compiled = CLIENT.compile(clear_program())

    approval_compiled_decoded = base64.b64decode(approval_compiled['result'])
    clear_compiled_decoded = base64.b64decode(clear_compiled['result'])

    local_ints = 5
    local_bytes = 0
    global_ints = 6
    global_bytes = 0
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    on_complete = transaction.OnComplete.NoOpOC.real

    params = CLIENT.suggested_params()

    txn = transaction.ApplicationCreateTxn(
        creator_address,
        params,
        on_complete,
        approval_compiled_decoded,
        clear_compiled_decoded,
        global_schema,
        local_schema
    )

    txn_signed = txn.sign(creator_pk)
    txn_id = CLIENT.send_transactions([txn_signed])

    app_id = wait_for_confirmation(txn_id)['application-index']
    return app_id


def initialize(
    creator_address,
    creator_priv_key,
    facilitator_address,
    facilitator_priv_key,
    app_id
):
    params = CLIENT.suggested_params()
    app_address = get_application_address(app_id)

    txn1, _ = prepare_transfer_algos(
        creator_address,
        app_address,
        settings.ALGO_OPT_IN_AMOUNT
    )
    txn2 = transaction.ApplicationNoOpTxn(
        creator_address,
        params,
        app_id,
        ["INIT"],
        foreign_assets=[settings.ALGO_ASSET]
    )
    txn3 = opt_in(facilitator_address, app_id, 1)

    txn_id = sign_send_atomic_trasfer(
        [creator_priv_key, creator_priv_key, facilitator_priv_key],
        [txn1, txn2, txn3]
    )
    wait_for_confirmation(txn_id)


def opt_in(address, app_id, role):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationOptInTxn(address, params, app_id, [role])
    return txn


def opt_out(address, app_id):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationCloseOutTxn(address, params, app_id)
    return txn


def invest(address, priv_key, app_id, amount, asset=settings.ALGO_ASSET):
    params = CLIENT.suggested_params()
    app_address = get_application_address(app_id)

    txn1 = opt_in(address, app_id, 2)
    txn2 = transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        ["INVEST"],
        foreign_assets=[asset]
    )
    txn3, _ = prepare_transfer_assets(
        address,
        app_address,
        amount,
        asset=asset
    )

    txn_id = sign_send_atomic_trasfer(priv_key, [txn1, txn2, txn3])
    wait_for_confirmation(txn_id)


def start(address, priv_key, app_id, start, end, fac_adm_funds):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        ["START", start, end, int(fac_adm_funds * 1000000)],
    )

    txn_signed = txn.sign(priv_key)
    txn_id = CLIENT.send_transactions([txn_signed])
    wait_for_confirmation(txn_id)


def withdraw(address, app_id):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        ["WITHDRAW"],
        foreign_assets=[settings.ALGO_ASSET]
    )
    return txn


def delete(address, app_id):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationDeleteTxn(
        address,
        params,
        app_id,
        foreign_assets=[settings.ALGO_ASSET]
    )
    return txn


def opted_in_addresses(app_id):
    accounts = INDEXER.accounts(application_id=app_id)['accounts']
    print("ACCS", accounts)
    role_addresses = defaultdict(list)
    for account in accounts:
        apps_local_state = account['apps-local-state']
        for app_local_state in apps_local_state:
            print("AID", app_local_state['id'], app_id)
            if app_local_state['id'] == app_id:
                for key_value in app_local_state['key-value']:
                    print("KEY V", base64.b64decode(key_value['key']).decode())
                    if base64.b64decode(key_value['key']).decode() == "role":
                        role_addresses[key_value['value']
                                       ['uint']].append(account['address'])
    return role_addresses


def join(address, priv_key, app_id):
    txn = opt_in(address, app_id, 3)
    txn_signed = txn.sign(priv_key)
    txn_id = CLIENT.send_transactions([txn_signed])
    wait_for_confirmation(txn_id)


def approval(address, priv_key, beneficiary_address, value, app_id):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        ["JOIN", value],
        foreign_assets=[settings.ALGO_ASSET],
        accounts=[beneficiary_address]
    )
    txn_signed = txn.sign(priv_key)
    txn_id = CLIENT.send_transactions([txn_signed])
    wait_for_confirmation(txn_id)


def get_beneficiaries(app_id):
    transactions = INDEXER.search_transactions(application_id=app_id)['transactions']
    beneficiaries = dict()
    for transaction in transactions:
        for local_state_delta in transaction.get('local-state-delta', []):
            for delta in local_state_delta['delta']:
                if base64.b64decode(delta['key']).decode() == "role" and beneficiaries.get(local_state_delta['address'], None) is None and delta['value']['uint'] == 3:
                    beneficiaries[local_state_delta['address']] = {
                        "approval": 0, 
                        "round-time": transaction['round-time'],
                        "optin_txid": transaction['id']
                    }
                elif base64.b64decode(delta['key']).decode() == "join":
                    beneficiaries[local_state_delta['address']]['approval'] = delta['value']['uint']
                    beneficiaries[local_state_delta['address']]['approval_txid'] = transaction['id']
    return beneficiaries

def work(address, priv_key, activity_id, amount, app_id):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        ["WORK", amount],
        note=f"W|W|{activity_id}"
    )
    txn_signed = txn.sign(priv_key)
    txn_id = CLIENT.send_transactions([txn_signed])
    wait_for_confirmation(txn_id)

def verify(address, priv_key, beneficiary_address, activity_id, amount, value, app_id):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        ["VERIFY", amount, value],
        note=f"W|V|{activity_id}",
        foreign_assets=[settings.ALGO_ASSET],
        accounts=[beneficiary_address]
    )
    txn_signed = txn.sign(priv_key)
    txn_id = CLIENT.send_transactions([txn_signed])
    wait_for_confirmation(txn_id)