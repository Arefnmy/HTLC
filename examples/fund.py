from datetime import datetime

from bitcoinutils.transactions import TxInput, Transaction, TxOutput, TxWitnessInput
from bitcoinutils.utils import to_satoshis

from network import push_tx
from participant import ALICE, BOB
from htlc import HTLC
from secret import Secret
from utils import build_fund_script

# END_TIME = int(datetime.now().timestamp()) + 3600  # one hour later
END_TIME = 1692716702
print('End Time : ', END_TIME)

TX_ID = '6c8fa79daae26c185247188ed0029c45e7fe1a938cb3d57ec92520f1f600ea6c'
TXOUT_INDEX = 1
AMOUNT = 0.000008

alice_secret = Secret.from_string('Alice Secret')
alice_htlc = HTLC('testnet', alice_secret.secret_hash_hex(),
                  ALICE.address, BOB.address, END_TIME)

txin = TxInput(TX_ID, TXOUT_INDEX)
# remaining amounts are fee
txout = TxOutput(to_satoshis(AMOUNT), build_fund_script(alice_htlc.script))

tx = Transaction([txin], [txout], has_segwit=True)

sig = ALICE.private_key.sign_segwit_input(tx, 0, ALICE.address.to_script_pub_key(), to_satoshis(0.00001))
tx.witnesses.append(TxWitnessInput([sig, ALICE.public_key.to_hex()]))

print('Transaction ID : ', tx.get_txid())
print(tx)
print(tx.serialize())
response = push_tx(tx.serialize())
print(response)
