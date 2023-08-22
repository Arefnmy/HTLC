from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, TxOutput, Transaction
from bitcoinutils.utils import to_satoshis

from participant import ALICE, BOB
from htlc import HTLC
from secret import Secret
from utils import build_refund_script

TX_ID = 'd6079f263cec46192f1f139de52229925c39e9eda814d67a1307058e10a06edd'
UTXO_INDEX = 0
AMOUNT = 0.09
END_TIME = 1691713271

ALICE_SECRET = Secret.from_string('Alice Secret')
print('Secret hex : ', ALICE_SECRET.secret_hex())

alice_htlc = HTLC('testnet', ALICE_SECRET.secret_hash_hex(),
                  ALICE.address, BOB.address, END_TIME)
# set nSequences and nLockTime based on bip0065
txin = TxInput(TX_ID, UTXO_INDEX, sequence='fffffffe')

txout = TxOutput(to_satoshis(AMOUNT), ALICE.address.to_script_pub_key())

tx = Transaction([txin], [txout], locktime=hex(END_TIME)[2:])

sig = ALICE.private_key.sign_input(tx, 0, alice_htlc.script)
txin.script_sig = Script(build_refund_script(sig, ALICE.public_key.to_hex(), alice_htlc.script))

print('Transaction ID : ', tx.get_txid())
print(tx)
