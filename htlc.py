from bitcoinutils.script import Script as BTC_Script
from litecoinutils.script import Script as LTC_Scipt
from bitcoinutils.transactions import TxOutput as BTC_TxOutput
from litecoinutils.transactions import TxOutput as LTC_TxOutput

from secret import Secret


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
                                                                 endtime=str(end_time),
                                                                 sender_address_hash=self.sender_address.to_hash160()).split())
        elif network == 'ltc-test':
            self.script = LTC_Scipt(HTLC.script_template.format(secret_hash=secret_hash,
                                                                recipient_address_hash=self.recipient_address.to_hash160(),
                                                                endtime=str(end_time),
                                                                sender_address_hash=self.sender_address.to_hash160()).split())

    def build_fund_utxo(self, amount):
        if self.network == 'btc-test':
            return BTC_TxOutput(amount, self.script.to_p2sh_script_pub_key())
        elif self.network == 'ltc-test':
            return LTC_TxOutput(amount, self.script.to_p2sh_script_pub_key())
        else:
            raise NotImplemented

    def build_withdraw_utxo(self):
        raise NotImplemented


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

    # move methods to utils
    @staticmethod
    def extract_secret_hash(tx, network=None):
        pass

    @staticmethod
    def extract_secret(tx, secret_hash: str, network=None):  # tx hash
        txin = tx.inputs[0]  # TODO
        secret_pushed_hex = txin.script_sig.get_script()[2]  # TODO
        secret_pushed = Secret.from_hex(secret_pushed_hex)
        if secret_pushed.secret_hash_hex() != secret_hash:
            raise ValueError('Secret Hash is invalid!')
        return secret_pushed
