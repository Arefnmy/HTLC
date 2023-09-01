from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.keys import PrivateKey
from bitcoinutils.hdwallet import HDWallet
from test_framework.musig import generate_musig_key
def main():
    setup('testnet')

    #######################
    # Construct the input #
    #######################

    # get an HDWallet wrapper object by extended private key and path
    xprivkey = "tprv8ZgxMBicQKsPdQR9RuHpGGxSnNq8Jr3X4WnT6Nf2eq7FajuXyBep5KWYpYEixxx5XdTm1Ntpe84f3cVcF7mZZ7mPkntaFXLGJD2tS7YJkWU"
    path = "m/86'/1'/0'/0/5"
    hdw = HDWallet(xprivkey, path)
    internal_priv = hdw.get_private_key()
    print('From Private key:', internal_priv.to_wif())

    internal_pub = internal_priv.get_public_key()
    print('From Public key:', internal_pub.to_hex())

    from_address = internal_pub.get_taproot_address()
    print('From Taproot address:', from_address.to_string())

    # UTXO of fromAddress
    txid = '29afd65f1aeeab4e4d655b148776fe0097acc617492b0c3f3950b6a95be20f39'
    vout = 0

    # create transaction input from tx id of UTXO
    tx_in = TxInput(txid, vout)

    # all amounts are needed to sign a taproot input
    # (depending on sighash)
    amount = to_satoshis(0.00004)
    amounts = [ amount ]

    # all scriptPubKeys (in hex) are needed to sign a taproot input
    # (depending on sighash but always of the spend input)
    scriptPubkey = from_address.to_script_pub_key()
    utxos_scriptPubkeys = [ scriptPubkey ]

    ########################
    # Construct the output #
    ########################

    hdw.from_path("m/86'/1'/0'/0/7")
    to_priv = hdw.get_private_key()
    print('Send to Private key', to_priv.to_wif())
    to_pub = to_priv.get_public_key()




    privkey_tr_script_A = PrivateKey('cSW2kQbqC9zkqagw8oTYKFTozKuZ214zd6CMTDs4V32cMfH3dgKa')
    pubkey_tr_script_A = privkey_tr_script_A.get_public_key()
    privkey_tr_script_B = PrivateKey('cSv48xapaqy7fPs8VvoSnxNBNA2jpjcuURRqUENu3WVq6Eh4U3JU')
    pubkey_tr_script_B = privkey_tr_script_B.get_public_key().get_byte()
    privkey_tr_script_C = PrivateKey('cRkZPNnn3jdr64o3PDxNHG68eowDfuCdcyL6nVL4n3czvunuvryC')
    pubkey_tr_script_C = privkey_tr_script_C.get_public_key().get_byte()
    pubkeys=[pubkey_tr_script_A, pubkey_tr_script_B]



    c_map, pubkey_agg = generate_musig_key(pubkeys)
    privkeyA_c = privkey_tr_script_A * c_map[pubkey_tr_script_A]
    privkeyB_c = privkey_tr_script_B * c_map[pubkey_tr_script_B ]
    pubkeyA_c = pubkey_tr_script_A * c_map[pubkey_tr_script_A]
    pubkeyB_c = pubkey_tr_script_B * c_map[pubkey_tr_script_B]

    # Determine if the private and public keys need to be negated.
    # Hint: The aggregate public key is the one that needs to be valid.
    if pubkey_agg.get_y() % 2 != 0:
        privkeyA_c.negate()
        privkeyB_c.negate()
        pubkeyA_c.negate()
        pubkeyB_c.negate()
        pubkey_agg.negate()

    print('ssssssssssssssssssssssssssssssssssssssss')
    print(pubkey_agg.get_x())
    tr_script_p2pk_C_B = Script([pubkey_tr_script_C.to_x_only_hex(),'OP_CHECKSIGVERIFY',pubkey_tr_script_B.to_x_only_hex() , 'OP_CHECKSIG'])
    tr_script_p2pk_A_C = Script([pubkey_tr_script_C.to_x_only_hex(),'OP_CHECKSIGVERIFY',pubkey_tr_script_A.to_x_only_hex() , 'OP_CHECKSIG'])
    tr_script_p2pk_B_A =Script([pubkey_agg.get_x(), 'OP_CHECKSIG'])

    # tapleafs in order
    #                  TB_ABC
    #                  /     \
    #                 /       \
    #                /\        \
    #               /  \        \
    #              /    \        \
    #        TL_A_C    TL_B_A    TL_C_B
    all_leafs = [ [tr_script_p2pk_A_C, tr_script_p2pk_B_A], tr_script_p2pk_C_B ]

    # taproot script path address
    to_address = to_pub.get_taproot_address(all_leafs)
    print('To Taproot script address', to_address.to_string())

    # create transaction output
    tx_out = TxOutput(to_satoshis(0.0000035), to_address.to_script_pub_key())

    # create transaction without change output - if at least a single input is
    # segwit we need to set has_segwit=True
    tx = Transaction([tx_in], [tx_out], has_segwit=True)


    print("\nRaw transaction:\n" + tx.serialize())
    print('\ntxid: ' + tx.get_txid())
    print('\ntxwid: ' + tx.get_wtxid())

    # sign taproot input
    # to create the digest message to sign in taproot we need to
    # pass all the utxos' scriptPubKeys and their amounts
    sig = internal_priv.sign_taproot_input(tx, 0, utxos_scriptPubkeys, amounts)

    tx.witnesses.append( TxWitnessInput([ sig ]) )

    # print raw signed transaction ready to be broadcasted
    print("\nRaw signed transaction:\n" + tx.serialize())

    print("\nTxId:", tx.get_txid())
    print("\nTxwId:", tx.get_wtxid())
    print("\nSize:", tx.get_size())
    print("\nvSize:", tx.get_vsize())

if __name__ == "__main__":
    main()