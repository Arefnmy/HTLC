from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, TxOutput, Transaction
from bitcoinutils.utils import to_satoshis

from participant import ALICE, BOB
from htlc import HTLC
from secret import Secret
from utils import build_refund_script

TX_ID = 'd503a62d789a35a74fe4b262cf41218d96fb2fbb8d37e5e4345aaebfbf3e6f9b'
UTXO_INDEX = 0
AMOUNT = 0.09
END_TIME = 1691417604

ALICE_SECRET = Secret.from_string('Alice Secret')
print('Secret hex : ', ALICE_SECRET.secret_hex())

alice_htlc = HTLC('btc-test', ALICE_SECRET.secret_hash_hex(),
                  ALICE.address, BOB.address, END_TIME)
txin = TxInput(TX_ID, UTXO_INDEX)

txout = TxOutput(to_satoshis(AMOUNT), ALICE.address.to_script_pub_key())

tx = Transaction([txin], [txout])

sig = ALICE.private_key.sign_input(tx, 0, alice_htlc.script)
txin.script_sig = Script(build_refund_script(sig, ALICE.public_key.to_hex(), alice_htlc.script.script))

print('Transaction ID : ', tx.get_txid())
print(tx)
