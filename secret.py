from hashlib import sha256
from binascii import unhexlify


class Secret:

    def __init__(self, sec: bytes):
        self.sec = sec

    @classmethod
    def from_string(cls, s):
        return cls(sha256(s.encode()).digest())

    @classmethod
    def from_hex(cls, s):
        return cls(unhexlify(s))

    def secret_hex(self):
        return self.sec.hex()

    def secret_hash_hex(self):
        return sha256(self.sec).hexdigest()
