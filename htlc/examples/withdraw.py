from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, TxOutput, Transaction
from bitcoinutils.utils import to_satoshis

from htlc.examples.participant import ALICE, BOB
from htlc.htlc import HTLC
from network import push_tx
from htlc.secret import Secret
from htlc.utils import build_withdraw_script

TX_ID = '0ba41d5e7e500526915b2865e8d154a10e3366eb1069168925f6dd4fe5dcff62'
UTXO_INDEX = 0
AMOUNT = 0.00002
END_TIME = 1692795816
SECRET = Secret.from_hex('70b02494643d5084471db6ed484ef2332477ecaeb7d465b4fd1d096b11eb6da8')

htlc = HTLC('testnet', SECRET.secret_hash_hex(),
            ALICE.address, BOB.address, END_TIME)
txin = TxInput(TX_ID, UTXO_INDEX)

txout = TxOutput(to_satoshis(AMOUNT), BOB.address.to_script_pub_key())

tx = Transaction([txin], [txout])

sig = BOB.private_key.sign_input(tx, 0, htlc.script)
txin.script_sig = Script(build_withdraw_script(sig, BOB.public_key.to_hex(), SECRET.secret_hex(), htlc.script))

print('Transaction : ', tx)
print('Transaction Hex : ', tx.serialize())

response = push_tx(tx.serialize())
print(response)
