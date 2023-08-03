import hashlib


class Secret:

    def __init__(self, sec: bytes):
        self.sec = sec

    @classmethod
    def from_string(cls, s):
        return cls(hashlib.sha256(s.encode()).digest())

    def secret_hex(self):
        return self.sec.hex()

    def secret_hash_hex(self):
        return hashlib.sha256(self.sec).hexdigest()
