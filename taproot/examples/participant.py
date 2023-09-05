from bitcoinutils.hdwallet import HDWallet
from bitcoinutils.setup import setup

setup('testnet')

# get an HDWallet wrapper object by extended private key and path
xprivkey = "tprv8ZgxMBicQKsPdQR9RuHpGGxSnNq8Jr3X4WnT6Nf2eq7FajuXyBep5KWYpYEixxx5XdTm1Ntpe84f3cVcF7mZZ7mPkntaFXLGJD2tS7YJkWU"
path = "m/86'/1'/0'/0/6"
hdw = HDWallet(xprivkey, path)
internal_priv = hdw.get_private_key()
print('From Private key:', internal_priv.to_wif())

internal_pub = internal_priv.get_public_key()
print('From Public key:', internal_pub.to_hex())

from_address = internal_pub.get_taproot_address()
print('From Taproot address:', from_address.to_string())
