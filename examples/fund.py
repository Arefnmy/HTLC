from datetime import datetime

from bitcoinutils.transactions import TxInput, Transaction, TxOutput, TxWitnessInput
from bitcoinutils.utils import to_satoshis

from network import push_tx
from participant import ALICE, BOB
from htlc import HTLC
from secret import Secret
from utils import build_fund_script, jsonify_htlc

END_TIME = int(datetime.now().timestamp()) + 3600  # one hour later
print('End Time : ', END_TIME)

TX_ID = 'e6e745ec4f09a97379bb714b622ce0cf7566b9a126f55de8c98f1446c06f9eb9'
TXOUT_INDEX = 1
AMOUNT = 0.00003

alice_secret = Secret.from_string('Alice Secret')
alice_htlc = HTLC('testnet', alice_secret.secret_hash_hex(),
                  ALICE.address, BOB.address, END_TIME)

txin = TxInput(TX_ID, TXOUT_INDEX)
# remaining amounts are fee
txout = TxOutput(to_satoshis(AMOUNT), build_fund_script(alice_htlc.script))

tx = Transaction([txin], [txout], has_segwit=True)

sig = ALICE.private_key.sign_segwit_input(tx, 0, ALICE.address.to_script_pub_key(), to_satoshis(0.00004))
tx.witnesses.append(TxWitnessInput([sig, ALICE.public_key.to_hex()]))

jsonify_htlc(alice_htlc, tx.get_txid(), 'Alice_HTLC')
print('Transaction : ', tx)
print('Transaction Hex : ', tx.serialize())

response = push_tx(tx.serialize())
print(response)
