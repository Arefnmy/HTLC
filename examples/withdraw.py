from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, TxOutput, Transaction
from bitcoinutils.utils import to_satoshis

from examples.participant import ALICE, BOB
from htlc import HTLC
from secret import Secret
from utils import build_withdraw_script

TX_ID = 'd6079f263cec46192f1f139de52229925c39e9eda814d67a1307058e10a06edd'
UTXO_INDEX = 0
AMOUNT = 0.09
END_TIME = 1691417604
SECRET = Secret.from_hex('70b02494643d5084471db6ed484ef2332477ecaeb7d465b4fd1d096b11eb6da8')

htlc = HTLC('testnet', SECRET.secret_hash_hex(),
            ALICE.address, BOB.address, END_TIME)
txin = TxInput(TX_ID, UTXO_INDEX)

txout = TxOutput(to_satoshis(AMOUNT), BOB.address.to_script_pub_key())

tx = Transaction([txin], [txout])

sig = BOB.private_key.sign_input(tx, 0, htlc.script)
txin.script_sig = Script(build_withdraw_script(sig, BOB.public_key.to_hex(), SECRET.secret_hex(), htlc.script))

print('Transaction ID : ', tx.get_txid())
print(tx)
