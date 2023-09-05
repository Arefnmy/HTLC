from network import push_tx
from participant import *
from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.keys import PrivateKey

setup('testnet')

# UTXO of from_address
txid = '29afd65f1aeeab4e4d655b148776fe0097acc617492b0c3f3950b6a95be20f39'
vout = 0

# create transaction input from tx id of UTXO
tx_in = TxInput(txid, vout)

# all amounts are needed to sign a taproot input
# (depending on sighash)
amount = to_satoshis(0.00004)
amounts = [amount]

# all scriptPubKeys (in hex) are needed to sign a taproot input
# (depending on sighash but always of the spend input)
scriptPubkey = from_address.to_script_pub_key()
utxos_scriptPubkeys = [scriptPubkey]

hdw.from_path("m/86'/1'/0'/0/7")
to_priv = hdw.get_private_key()
print('Send to Private key', to_priv.to_wif())
to_pub = to_priv.get_public_key()

# taproot script A is a simple P2PK with the following key
privkey_tr_script_A = PrivateKey('cSW2kQbqC9zkqagw8oTYKFTozKuZ214zd6CMTDs4V32cMfH3dgKa')
pubkey_tr_script_A = privkey_tr_script_A.get_public_key()
tr_script_p2pk_A = Script([pubkey_tr_script_A.to_x_only_hex(), 'OP_CHECKSIG'])

# taproot script B is a simple P2PK with the following key
privkey_tr_script_B = PrivateKey('cSv48xapaqy7fPs8VvoSnxNBNA2jpjcuURRqUENu3WVq6Eh4U3JU')
pubkey_tr_script_B = privkey_tr_script_B.get_public_key()
tr_script_p2pk_B = Script([pubkey_tr_script_B.to_x_only_hex(), 'OP_CHECKSIG'])

# tapleafs in order
#      TB_AB
#      /   \
#   TL_A  TL_B
all_leafs = [tr_script_p2pk_A, tr_script_p2pk_B]

# taproot script path address
to_address = to_pub.get_taproot_address(all_leafs)
print('To Taproot script address', to_address.to_string())

# create transaction output
tx_out = TxOutput(to_satoshis(0.000035), to_address.to_script_pub_key())

# create transaction without change output - if at least a single input is
# segwit we need to set has_segwit=True
tx = Transaction([tx_in], [tx_out], has_segwit=True)

# sign taproot input
# to create the digest message to sign in taproot we need to
# pass all the utxos's scriptPubKeys and their amounts
sig = internal_priv.sign_taproot_input(tx, 0, utxos_scriptPubkeys, amounts)
tx.witnesses.append(TxWitnessInput([sig]))

# print raw signed transaction ready to be broadcasted
print("Raw signed transaction:\n" + tx.serialize())
print("TxId:", tx.get_txid())

response = push_tx(tx.serialize())
print(response)
