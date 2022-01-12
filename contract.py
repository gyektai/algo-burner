from pyteal import *
import os

def approval_program():

    # the account can only transfer assets in amounts of 0
    # so it can opt in, but never do anything with what it receives
    program = And(
        Txn.type_enum() == TxnType.AssetTransfer,
        Txn.asset_amount() == Int(0)
    )

    return compileTeal(program, mode=Mode.Application, version=5)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path,"burnerProgram.teal"), "w") as f:
        f.write(approval_program())
