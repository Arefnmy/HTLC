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
CAROL = Participant(LTCPrivateKey.from_wif('cSYHjzm5wAkbrPxGPXj7nUcta4rAoqX2sVfCjweDWpFpfho46NpT'))

# Alice segwit address : tb1qys92059qewdrux85y0k433cjcrl3v0nqkyxnlc
# Bob segwit address : tb1qff9k79eefa0hrxa5sk3tz7ah3ved8cg4muvfws
# Carol segwit address : tltc1qdwwxh6z28ywy3gzass9uc9t4egjexq0dc7aat2
