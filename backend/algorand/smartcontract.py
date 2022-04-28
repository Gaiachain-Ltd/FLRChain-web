import base64
from algosdk.v2client import *
from algosdk.future import *
from algosdk.logic import *
from algosdk.util import *
from pyteal import *
from algorand.utils import (INDEXER, CLIENT, wait_for_confirmation, prepare_transfer_algos,
                            prepare_transfer_assets, sign_send_atomic_trasfer)
from django.conf import settings


NOTE_PAY_BEN_WORK = "P|W" #Pay for work
NOTE_PAY_FAC_ADM = "P|F" #Pay for fac adm funds
NOTE_PAYBACK_INV = "P|I" #Payback unspend funds
NOTE_PAY_BEN_BATCH = "P|B" #Pay batch
NOTE_CASHOUT_FAC = "C|F" #Cashout to facilitator
NOTE_CASHOUT_MOBILE = "C|M" #Cashout to mobile
NOTE_CASHOUT_ADDRESS = "C|A" # Cashout to wallet address
NOTE_INVESTMENT = "I|"
NOTE_WORK = "W|W"
NOTE_VERIFY = "W|V"
NOTE_BATCH = "W|B"


def approval_program():
    G_STATUS_KEY = Bytes("status")
    G_TOTAL_KEY = Bytes("total")
    G_ADM_KEY = Bytes("adm")
    G_DETAILS_KEY = Bytes("details")

    L_TOTAL_KEY = Bytes("total")
    L_ROLE_KEY = Bytes("role")
    L_JOIN_KEY = Bytes("join")
    L_COUNT_KEY = Bytes("count")

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
    is_finished = App.globalGet(G_STATUS_KEY) == FINISHED_STATUS

    is_opted_in = App.localGet(Txn.sender(), L_ROLE_KEY) != Int(0)

    is_creator = Global.creator_address() == Txn.sender()
    is_beneficiary = App.localGet(Txn.sender(), L_ROLE_KEY) == BENEFICIARY_ROLE
    is_investor = App.localGet(Txn.sender(), L_ROLE_KEY) == INVESTOR_ROLE
    is_facilitator = App.localGet(
        Txn.sender(), L_ROLE_KEY) == FACILILTATOR_ROLE

    projectBalance = AssetHolding.balance(
        Global.current_application_address(), Txn.assets[0])

    tmp_int = ScratchVar(TealType.uint64)

    @Subroutine(TealType.uint64)
    def is_accepted(account):
        return App.localGet(account, L_JOIN_KEY) == ACCEPTED_JOIN

    @Subroutine(TealType.none)
    def set_project_properties():
        return Seq([
            Assert(Txn.application_args.length() == Int(6)),
            Assert(Btoi(Txn.application_args[1]) <= Btoi(Txn.application_args[2])),
            App.globalPut(G_DETAILS_KEY, Concat(
                    Txn.application_args[1],
                    Bytes(";"),
                    Txn.application_args[2],
                    Bytes(";"),
                    Txn.application_args[3],
                    Bytes(";"),
                    Txn.application_args[5]
                )
            ),
            App.globalPut(G_ADM_KEY, Btoi(Txn.application_args[3])),
        ])

    @Subroutine(TealType.uint64)
    def facilitator_adm_fee_withdraw():
        return Minus(
            App.globalGet(G_ADM_KEY),
            App.localGet(Txn.sender(), L_TOTAL_KEY)
        )

    # OPT-IN USDC:
    on_init = Seq([
        Assert(is_facilitator),
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
        set_project_properties(),
        Approve()
    ])

    # Invest:
    on_invest = Seq([
        Assert(is_investor),
        Assert(Or(is_initialized, is_started)),
        Assert(Txn.note() == Bytes(NOTE_INVESTMENT)),
        Assert(
            And(
                Gtxn[Global.group_size()-Int(1)].type_enum() == TxnType.AssetTransfer,
                Gtxn[Global.group_size()-Int(1)].xfer_asset() == Txn.assets[0],
                Gtxn[Global.group_size()-Int(1)].asset_receiver() == Global.current_application_address(),
                Gtxn[Global.group_size()-Int(1)].asset_amount() == Btoi(Txn.application_args[1])
            )
        ),
        App.globalPut(
            G_TOTAL_KEY,
            Add(
                App.globalGet(G_TOTAL_KEY),
                Gtxn[Global.group_size()-Int(1)].asset_amount()
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

    on_join = Seq([
        Assert(is_facilitator),
        Assert(Or(is_initialized, is_started)),
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
        Assert(is_beneficiary),
        Assert(is_started),
        Assert(Len(Txn.note()) > Int(3)),
        Assert(Extract(Txn.note(), Int(0), Int(3)) == Bytes(NOTE_WORK)),
        Assert(is_accepted(Txn.sender())),
        Approve()
    ])

    on_verify = Seq([
        Assert(is_facilitator),
        Assert(is_started),
        Assert(Len(Txn.note()) > Int(3)),
        Assert(Extract(Txn.note(), Int(0), Int(3)) == Bytes(NOTE_VERIFY)),
        Assert(is_accepted(Txn.accounts[1])),
        Assert(
            Or(
                Btoi(Txn.application_args[2]) == ACCEPTED_VERIFY,
                Btoi(Txn.application_args[2]) == REJECTED_VERIFY
            )
        ),
        If(Btoi(Txn.application_args[2]) == ACCEPTED_VERIFY).
        Then(
            Seq([
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: Txn.assets[0],
                    TxnField.asset_receiver: Txn.accounts[1],
                    TxnField.asset_amount: Btoi(Txn.application_args[1]),
                    TxnField.note: Bytes(NOTE_PAY_BEN_WORK)
                }),
                InnerTxnBuilder.Submit(),
            ])
        ),
        Approve()
    ])

    # Project update:
    # Update project properties.
    on_update = Seq([
        Assert(is_facilitator),
        set_project_properties(),
        App.globalPut(G_STATUS_KEY, Btoi(Txn.application_args[4])),
        If(is_started). # Send ADM FEE
        Then(
            Seq([
                tmp_int.store(facilitator_adm_fee_withdraw()),
                If(tmp_int.load() > Int(0)).
                Then(
                    Seq([
                        InnerTxnBuilder.Begin(),
                        InnerTxnBuilder.SetFields({
                            TxnField.type_enum: TxnType.AssetTransfer,
                            TxnField.xfer_asset: Txn.assets[0],
                            TxnField.asset_receiver: Txn.sender(),
                            TxnField.asset_amount: tmp_int.load(),
                            TxnField.note: Bytes(NOTE_PAY_FAC_ADM)
                        }),
                        InnerTxnBuilder.Submit(),
                        App.localPut(
                            Txn.sender(), 
                            L_TOTAL_KEY, 
                            App.globalGet(G_ADM_KEY)
                        )
                    ])
                )
            ])
        ),
        Approve()
    ])

    on_batch = Seq([
        Assert(is_facilitator),
        Assert(is_started),
        Assert(App.localGet(Txn.accounts[1], L_ROLE_KEY) == BENEFICIARY_ROLE),
        Assert(Len(Txn.note()) > Int(3)),
        Assert(Extract(Txn.note(), Int(0), Int(3)) == Bytes(NOTE_BATCH)),
        projectBalance,
        If(projectBalance.value() >= Btoi(Txn.application_args[1])).
        Then(Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Txn.assets[0],
                TxnField.asset_receiver: Txn.accounts[1],
                TxnField.asset_amount: Btoi(Txn.application_args[1]),
                TxnField.note: Bytes(NOTE_PAY_BEN_BATCH)
            }),
            InnerTxnBuilder.Submit(),
        ])).Else(Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Txn.assets[0],
                TxnField.asset_receiver: Txn.accounts[1],
                TxnField.asset_amount: Int(0),
                TxnField.note: Bytes(NOTE_PAY_BEN_BATCH)
            }),
            InnerTxnBuilder.Submit(),
        ])),
        Approve()
    ])

    handle_noop = Cond(
        [Txn.application_args[0] == Bytes("INIT"), on_init],
        [Txn.application_args[0] == Bytes("INVEST"), on_invest],
        [Txn.application_args[0] == Bytes("JOIN"), on_join],
        [Txn.application_args[0] == Bytes("WORK"), on_work],
        [Txn.application_args[0] == Bytes("VERIFY"), on_verify],
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

    # OPT-IN application:
    # Set local state "role". In this way we will identify users.
    handle_optin = Seq([
        Assert(Not(is_opted_in)),
        If(Btoi(Txn.application_args[0]) != FACILILTATOR_ROLE).
        Then(Assert(Or(is_initialized, is_started))),
        App.localPut(Txn.sender(), L_ROLE_KEY, Btoi(Txn.application_args[0])),
        Approve()
    ])

    handle_optout = Seq([
        If(
            And(
                And(is_investor, is_finished), 
                App.localGet(Txn.sender(), L_COUNT_KEY) >= Int(1)
            ),
            Seq([
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: Txn.assets[0],
                    TxnField.asset_receiver: Txn.sender(),
                    TxnField.asset_amount: Btoi(Txn.application_args[0]),
                    TxnField.note: Bytes(NOTE_PAYBACK_INV)
                }),
                InnerTxnBuilder.Submit(),
                App.localPut(Txn.sender(), L_COUNT_KEY, Int(0))
            ])
        ),
        Approve()
    ])

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_optout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )
    return compileTeal(program, Mode.Application, version=6)


def clear_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=6)


def create(creator_address, creator_pk):
    approval_compiled = CLIENT.compile(approval_program())
    clear_compiled = CLIENT.compile(clear_program())

    approval_compiled_decoded = base64.b64decode(approval_compiled['result'])
    clear_compiled_decoded = base64.b64decode(clear_compiled['result'])

    local_ints = 4
    local_bytes = 0
    global_ints = 3
    global_bytes = 1
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


def update_contract(creator_address, creator_pk, app_id):
    approval_compiled = CLIENT.compile(approval_program())
    clear_compiled = CLIENT.compile(clear_program())

    approval_compiled_decoded = base64.b64decode(approval_compiled['result'])
    clear_compiled_decoded = base64.b64decode(clear_compiled['result'])

    params = CLIENT.suggested_params()

    txn = transaction.ApplicationUpdateTxn(
        creator_address,
        params,
        app_id,
        approval_compiled_decoded,
        clear_compiled_decoded,

    )

    txn_signed = txn.sign(creator_pk)
    txn_id = CLIENT.send_transactions([txn_signed])

    wait_for_confirmation(txn_id)


def initialize(
    creator_address,
    creator_priv_key,
    facilitator_address,
    facilitator_priv_key,
    app_id,
    start,
    end,
    fac_adm_funds,
    status,
    total
):
    params = CLIENT.suggested_params()
    app_address = get_application_address(app_id)

    txn1 = prepare_transfer_algos(
        creator_address,
        app_address,
        settings.ALGO_OPT_IN_AMOUNT
    )
    txn2 = opt_in(facilitator_address, app_id, 1)
    txn3 = transaction.ApplicationNoOpTxn(
        facilitator_address,
        params,
        app_id,
        [
            "INIT", 
            start, 
            end, 
            algos_to_microalgos(fac_adm_funds), 
            status,
            algos_to_microalgos(total)
        ],
        foreign_assets=[settings.ALGO_ASSET]
    )
    
    txn_id = sign_send_atomic_trasfer(
        [creator_priv_key, facilitator_priv_key, facilitator_priv_key],
        [txn1, txn2, txn3]
    )
    wait_for_confirmation(txn_id)


def opt_in(address, app_id, role):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationOptInTxn(address, params, app_id, [role])
    return txn


def opt_out(address, app_id, amount):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationCloseOutTxn(
        address, 
        params, 
        app_id,
        [algos_to_microalgos(amount)],
        foreign_assets=[settings.ALGO_ASSET])
    return txn


def invest(address, priv_key, app_id, amount, asset=settings.ALGO_ASSET, include_opt_in=True):
    params = CLIENT.suggested_params()
    app_address = get_application_address(app_id)
    
    txns = list()
    if include_opt_in:
        txns.append(opt_in(address, app_id, 2))
        
    txns.append(transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        ["INVEST", algos_to_microalgos(amount)],
        foreign_assets=[asset],
        note=NOTE_INVESTMENT
    ))
    txns.append(prepare_transfer_assets(
        address,
        app_address,
        amount,
        asset=asset
    ))

    txn_id = sign_send_atomic_trasfer(priv_key, txns)
    wait_for_confirmation(txn_id)


def update(address, priv_key, app_id, start, end, fac_adm_funds, status, total):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        [
            "UPDATE", 
            start, 
            end, 
            algos_to_microalgos(fac_adm_funds), 
            status,
            algos_to_microalgos(total)
        ],
        foreign_assets=[settings.ALGO_ASSET]
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


def delete_application(address, app_id):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationDeleteTxn(
        address,
        params,
        app_id,
        foreign_assets=[settings.ALGO_ASSET]
    )
    return txn


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
                        "status": 0,
                        "sync": 0,
                        "round-time": transaction['round-time'],
                        "optin_txid": transaction['id']
                    }
                elif base64.b64decode(delta['key']).decode() == "join":
                    beneficiaries[local_state_delta['address']].update({
                        "status": delta['value']['uint'],
                        "approval_txid": transaction['id']
                    })
    return beneficiaries


def work(address, priv_key, activity_id, amount, app_id):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        ["WORK", algos_to_microalgos(amount)],
        note=f"{NOTE_WORK}|{activity_id}"
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
        ["VERIFY", algos_to_microalgos(amount), value],
        note=f"{NOTE_VERIFY}|{activity_id}",
        foreign_assets=[settings.ALGO_ASSET],
        accounts=[beneficiary_address]
    )
    txn_signed = txn.sign(priv_key)
    txn_id = CLIENT.send_transactions([txn_signed])
    wait_for_confirmation(txn_id)


def batch(address, beneficiary_address, task_id, amount, app_id):
    params = CLIENT.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        address,
        params,
        app_id,
        ["BATCH", algos_to_microalgos(amount)],
        note=f"{NOTE_BATCH}|{task_id}",
        foreign_assets=[settings.ALGO_ASSET],
        accounts=[beneficiary_address]
    )
    return txn