from network import push_tx
from participant import *
from bitcoinutils.utils import to_satoshis
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput

from test_framework.key import generate_key_pair
from test_framework.messages import sha256
from test_framework.musig import generate_musig_key


def create_2of2_agg_pubkey(privkey1, pubkey1, privkey2, pubkey2):
    pubkeys = [pubkey1, pubkey2]

    c_map, pubkey_agg = generate_musig_key(pubkeys)

    # Multiply key pairs by challenge factor
    privkey1_c = privkey1 * c_map[pubkey1]
    privkey2_c = privkey2 * c_map[pubkey2]
    pubkey1_c = pubkey1 * c_map[pubkey1]
    pubkey2_c = pubkey2 * c_map[pubkey2]
    # Determine if the private and public keys need to be negated.
    if pubkey_agg.get_y() % 2 != 0:
        privkey1_c.negate()
        privkey2_c.negate()
        pubkey1_c.negate()
        pubkey2_c.negate()
        pubkey_agg.negate()

    return pubkey_agg


# UTXO of fromAddress
txid = '2afc7066492fbb83ea4648ce430182de27f755f6e9c25890607f5c6ddac0f4a9'
vout = 1

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

privkey1, pubkey1 = generate_key_pair(sha256(b'key0'))
privkey2, pubkey2 = generate_key_pair(sha256(b'key1'))
privkey3, pubkey3 = generate_key_pair(sha256(b'key2'))

# create 2of2 musig scripts
tr_script_p2pk_B_A = Script([create_2of2_agg_pubkey(privkey1, pubkey1, privkey2, pubkey2).get_x(), 'OP_CHECKSIG'])
tr_script_p2pk_A_C = Script([create_2of2_agg_pubkey(privkey1, pubkey1, privkey3, pubkey3).get_x(), 'OP_CHECKSIG'])
tr_script_p2pk_C_B = Script([create_2of2_agg_pubkey(privkey3, pubkey3, privkey2, pubkey2).get_x(), 'OP_CHECKSIG'])

# tapleafs in order
#                  TB_ABC
#                  /     \
#                 /       \
#                /\        \
#               /  \        \
#              /    \        \
#        TL_A_C    TL_B_A    TL_C_B
all_leafs = [[tr_script_p2pk_A_C, tr_script_p2pk_B_A], tr_script_p2pk_C_B]

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
