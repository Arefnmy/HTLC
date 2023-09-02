from bitcoinutils.constants import ABSOLUTE_TIMELOCK_SEQUENCE
from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, TxOutput, Transaction
from bitcoinutils.utils import to_satoshis

from network import push_tx
from participant import ALICE, BOB
from htlc.htlc import HTLC
from htlc.secret import Secret
from htlc.utils import build_refund_script

TX_ID = 'e6473ae1519a0f41d1618d03b2d7068a98d270988e48709502f003d1a591719d'
UTXO_INDEX = 0
AMOUNT = 0.00002
END_TIME = 1692801170

ALICE_SECRET = Secret.from_string('Alice Secret')
print('Secret hex : ', ALICE_SECRET.secret_hex())

alice_htlc = HTLC('testnet', ALICE_SECRET.secret_hash_hex(),
                  ALICE.address, BOB.address, END_TIME)
# set nSequences and nLockTime based on bip0065
txin = TxInput(TX_ID, UTXO_INDEX, sequence=ABSOLUTE_TIMELOCK_SEQUENCE)

txout = TxOutput(to_satoshis(AMOUNT), ALICE.address.to_script_pub_key())

tx = Transaction([txin], [txout], END_TIME.to_bytes(length=4, byteorder='little'))

sig = ALICE.private_key.sign_input(tx, 0, alice_htlc.script)
txin.script_sig = Script(build_refund_script(sig, ALICE.public_key.to_hex(), alice_htlc.script))

print('Transaction : ', tx)
print('Transaction Hex : ', tx.serialize())

response = push_tx(tx.serialize())
print(response)
