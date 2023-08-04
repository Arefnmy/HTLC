from datetime import datetime

from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, Transaction
from bitcoinutils.utils import to_satoshis

from examples.participant import ALICE, BOB
from htlc import HTLC
from secret import Secret

END_TIME = int(datetime.now().timestamp()) + 3600  # one hour later
print(END_TIME)

TX_ID = 'fb48f4e23bf6ddf606714141ac78c3e921c8c0bebeb7c8abb2c799e9ff96ce6c'
TXOUT_INDEX = 0
AMOUNT = 0.09

alice_secret = Secret.from_string('Alice Secret')
alice_htlc = HTLC('btc-test', alice_secret.secret_hash_hex(),
                  ALICE.address, BOB.address, END_TIME)

txin = TxInput(TX_ID, TXOUT_INDEX)
txout = alice_htlc.build_fund_utxo(to_satoshis(AMOUNT))

tx = Transaction([txin], [txout])

sig = ALICE.private_key.sign_input(tx, 0, ALICE.address.to_script_pub_key())
txin.script_sig = Script([sig, ALICE.public_key.to_hex()])

print(tx.get_txid())
print(tx)