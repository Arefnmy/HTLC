from bitcoinutils.keys import PrivateKey as BTCPrivateKey
from bitcoinutils.setup import setup as BTC_setup
from litecoinutils.keys import PrivateKey as LTCPrivateKey
from litecoinutils.setup import setup as LTC_setup


class Participant:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = private_key.get_public_key()
        self.address = self.public_key.get_address()


BTC_setup('testnet')
LTC_setup('testnet')

ALICE = Participant(BTCPrivateKey.from_wif('cNLwCLQe7AVtTBALB2mmAohD9qyTS3wtN6fQszoaJUyhgCgqwskW'))
BOB = Participant(BTCPrivateKey.from_wif('cQWgi89zVdiwnJLmQRKPquFkoJ36avdsKbpvMW5gLC2HtVjdBbd1'))
CAROL = Participant(LTCPrivateKey.from_wif('TBSVWXcs9ttsRhBHHv1hmULnj2W32aGkH9jVGYvWGDLjpjkAxEqK'))
