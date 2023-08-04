from bitcoinutils.keys import PrivateKey as BTCPrivateKey
from litecoinutils.keys import PrivateKey as LTCPrivateKey


class Participant:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = private_key.get_public_key()
        self.address = self.public_key.get_address()


ALICE = Participant(BTCPrivateKey())
BOB = Participant(BTCPrivateKey())
CAROL = Participant(LTCPrivateKey())
