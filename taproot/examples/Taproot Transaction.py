from network import push_tx
from participant import *
from bitcoinutils.utils import to_satoshis
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.keys import PrivateKey

# UTXO of from address
txid = '67e8c015625279f2d4268a7b15e8a6feef39a86ed4f5c14acbd260f612b8c44a'
vout = 1

# create transaction input from tx id of UTXO
tx_in = TxInput(txid, vout)

# all amounts are needed to sign a taproot input
# (depending on sighash)
amount = to_satoshis(0.00009658)
amounts = [amount]

# all scriptPubKeys (in hex) are needed to sign a taproot input
# (depending on sighash but always of the spend input)
scriptPubkey = from_address.to_script_pub_key()
utxos_scriptPubkeys = [scriptPubkey]


hdw.from_path("m/86'/1'/0'/0/7")
to_priv = hdw.get_private_key()
print('To Private key', to_priv.to_wif())
to_pub = to_priv.get_public_key()
print('To Public key', to_pub.to_hex())

# taproot script is a simple P2PK with the following keys

# tapleaf script p2pk script
privkey_tr_script = PrivateKey('cQwzrJyTNWbEwhPEmQ3Qoo4jSfHdHEtdbL4kNBgHUKhirgzcQw7G')
pubkey_tr_script = privkey_tr_script.get_public_key()
tr_script_p2pk = Script([pubkey_tr_script.to_x_only_hex(), 'OP_CHECKSIG'])

# taproot script path address
to_address = to_pub.get_taproot_address([[tr_script_p2pk]])
print('To Taproot script address', to_address.to_string())

# create transaction output
tx_out = TxOutput(to_satoshis(0.00009), to_address.to_script_pub_key())

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
