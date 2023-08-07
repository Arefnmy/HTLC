from datetime import datetime

from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, Transaction, TxOutput
from bitcoinutils.utils import to_satoshis

from participant import ALICE, BOB
from htlc import HTLC
from secret import Secret
from utils import build_fund_script

END_TIME = int(datetime.now().timestamp()) + 3600  # one hour later
print('End Time : ', END_TIME)

TX_ID = 'fb48f4e23bf6ddf606714141ac78c3e921c8c0bebeb7c8abb2c799e9ff96ce6c'
TXOUT_INDEX = 0
AMOUNT = 0.09
# fee , change output
alice_secret = Secret.from_string('Alice Secret')
alice_htlc = HTLC('btc-test', alice_secret.secret_hash_hex(),
                  ALICE.address, BOB.address, END_TIME)

txin = TxInput(TX_ID, TXOUT_INDEX)
txout = TxOutput(to_satoshis(AMOUNT), build_fund_script(alice_htlc.script))

tx = Transaction([txin], [txout])

sig = ALICE.private_key.sign_input(tx, 0, ALICE.address.to_script_pub_key())
txin.script_sig = Script([sig, ALICE.public_key.to_hex()])

print('Transaction ID : ', tx.get_txid())
print(tx)
