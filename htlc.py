from bitcoinutils.script import Script
from bitcoinutils.transactions import TxOutput

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

        self.script = Script(HTLC.script_template.format(secret_hash=secret_hash,
                                                         recipient_address_hash=self.recipient_address.to_hash160(),
                                                         endtime=str(end_time),
                                                         sender_address_hash=self.sender_address.to_hash160()).split())

    def build_fund_utxo(self, amount):
        txout = TxOutput(amount, self.script.to_p2sh_script_pub_key())
        return txout

    # def sign_refund_tx(self, tx, txin_index, private_key):
    #     sig = private_key.sign_input(tx, 0, self.script)
    #     tx.inputs[0].script_sig = Script([sig, self.script.to_hex()])
    #     return tx
