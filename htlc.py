from bitcoinutils.script import Script as BTC_Script
from litecoinutils.script import Script as LTC_Script


class HTLC:
    script_template = 'OP_IF OP_SHA256 {secret_hash} OP_EQUALVERIFY OP_DUP OP_HASH160' \
                      ' {recipient_address_hash} OP_EQUALVERIFY OP_CHECKSIG OP_ELSE ' \
                      '{endtime} OP_CHECKLOCKTIMEVERIFY OP_DROP OP_DUP OP_HASH160 {sender_address_hash}' \
                      ' OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF'

    def __init__(self, network: str, secret_hash, sender_address, recipient_address, end_time: int):
        self.network = network
        self.secret_hash = secret_hash
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.end_time = end_time

        # implement in separate classes
        if network == 'btc-test':
            self.script = BTC_Script(HTLC.script_template.format(secret_hash=secret_hash,
                                                                 recipient_address_hash=self.recipient_address.to_hash160(),
                                                                 endtime=hex(end_time)[2:],
                                                                 sender_address_hash=self.sender_address.to_hash160()).split())
        elif network == 'ltc-test':
            self.script = LTC_Script(HTLC.script_template.format(secret_hash=secret_hash,
                                                                 recipient_address_hash=self.recipient_address.to_hash160(),
                                                                 endtime=hex(end_time)[2:],
                                                                 sender_address_hash=self.sender_address.to_hash160()).split())


class Swap:

    def __init__(self, first_htlc: HTLC, second_htlc: HTLC):
        self.first_htlc = first_htlc
        self.second_htlc = second_htlc

    def evaluate(self, origin_time=None):
        if self.first_htlc.secret_hash != self.second_htlc.secret_hash:
            return False

        # check first duration >= 2* second duration
        # from datetime import datetime
        # now = datetime.now().timestamp()

        return self.first_htlc.end_time >= self.second_htlc.end_time + 24 * 3600  # 24 hours
