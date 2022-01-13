from pyteal import *
import os

def approval_program():

    # to check if the accounts already opted into the asset
    asset_balance = AssetHolding.balance(Txn.accounts[0], Txn.assets[0])
    opted = Seq(
        asset_balance,
        asset_balance.hasValue()
    )

    # the account can only opt in to assets on an application call
    # but won't ever be able to send them
    handle_noop = Seq(
        Assert(opted == Int(0)),
        InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Txn.assets[0],
                TxnField.receiver: Global.current_application_address(),
                TxnField.asset_amount: Int(0),
            }),
        InnerTxnBuilder.Submit(),
        Int(1)
    )

    # can't update, optin, closeout, delete
    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
        [Txn.on_completion() == OnComplete.NoOp, Return(handle_noop)]
    )

    return compileTeal(program, mode=Mode.Application, version=5)

# shouldn't be necessary since there's no opting in, but alway approve it
def clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, mode=Mode.Application, version=5)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path,"burnerProgram.teal"), "w") as f:
        f.write(approval_program())
    
    with open(os.path.join(path,"clearBurnerProgram.teal"), "w") as f:
        f.write(clear_state_program())
