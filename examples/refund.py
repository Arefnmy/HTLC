from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, TxOutput, Transaction
from bitcoinutils.utils import to_satoshis

from examples.participant import ALICE, BOB
from htlc import HTLC
from secret import Secret

TX_ID = '0fe3eac00c2d0d5e112da1df779e3b5fd1bde91a8d2a16ba797d3ba6329393e2'
UTXO_INDEX = 0
AMOUNT = 0.09
END_TIME = 1691151553
ALICE_SECRET = Secret.from_string('Alice Secret')

alice_htlc = HTLC('btc-test', ALICE_SECRET.secret_hash_hex(),
                  ALICE.address, BOB.address, END_TIME)
txin = TxInput(TX_ID, UTXO_INDEX)

txout = TxOutput(to_satoshis(AMOUNT), ALICE.address.to_script_pub_key())

tx = Transaction([txin], [txout])

sig = ALICE.private_key.sign_input(tx, 0, alice_htlc.script)
txin.script_sig = Script([sig, alice_htlc.script.to_hex()])  # TODO

print(tx.get_txid())
print(tx)