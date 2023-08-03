from bitcoinutils.keys import PrivateKey, P2pkhAddress
from datetime import datetime

from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, TxOutput, Transaction
from bitcoinutils.utils import to_satoshis

import hashlib
from secret import Secret
from htlc import HTLC


def main():
    END_TIME = int(datetime.now().timestamp()) + 3600  # one hour later
    TX_ID = 'fb48f4e23bf6ddf606714141ac78c3e921c8c0bebeb7c8abb2c799e9ff96ce6c'
    TXOUT_INDEX = 0
    AMOUNT = 0.09

    alice_private_key = PrivateKey()
    alice_public_key = alice_private_key.get_public_key()
    alice_address = alice_public_key.get_address()
    bob_private_key = PrivateKey()
    bob_public_key = bob_private_key.get_public_key()
    bob_address = bob_public_key.get_address()

    # Create Fund TX
    alice_htlc = HTLC('testnet', Secret.from_string('Alice secret'),
                      alice_address, bob_address, END_TIME)

    txin = TxInput(TX_ID, TXOUT_INDEX)
    txout = alice_htlc.build_fund_utxo(to_satoshis(AMOUNT))

    tx = Transaction([txin], [txout])

    sig = alice_private_key.sign_input(tx, 0, alice_address.to_script_pub_key())
    txin.script_sig = Script([sig, alice_public_key.to_hex()])

    # Create Refund TX
    utxo_id = tx.get_txid()
    utxo_index = 0
    txin = TxInput(utxo_id, utxo_index)

    txout = TxOutput(to_satoshis(AMOUNT), alice_address.to_script_pub_key())

    tx = Transaction([txin], [txout])

    sig = alice_private_key.sign_input(tx, 0, alice_htlc.script)
    txin.script_sig = Script([sig, alice_htlc.script.to_hex()])


if __name__ == '__main__':
    main()
