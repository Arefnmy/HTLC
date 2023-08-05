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
SECRET = Secret.from_hex('70b02494643d5084471db6ed484ef2332477ecaeb7d465b4fd1d096b11eb6da8')

htlc = HTLC('btc-test', SECRET.secret_hash_hex(),
            ALICE.address, BOB.address, END_TIME)
txin = TxInput(TX_ID, UTXO_INDEX)

txout = TxOutput(to_satoshis(AMOUNT), BOB.address.to_script_pub_key())

tx = Transaction([txin], [txout])

sig = BOB.private_key.sign_input(tx, 0, htlc.script)
txin.script_sig = Script([sig,  BOB.public_key.to_hex(), SECRET.secret_hex(), b'']
                         + htlc.script.script)
print(tx.get_txid())
print(tx)
