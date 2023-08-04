from bitcoinutils.keys import PrivateKey


class Participant:
    def __init__(self, private_key=PrivateKey()):
        self.private_key = private_key
        self.public_key = private_key.get_public_key()
        self.address = self.public_key.get_address()


ALICE = Participant()
BOB = Participant()
