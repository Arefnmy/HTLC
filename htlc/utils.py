import json

from secret import Secret


def build_fund_script(script):
    return script.to_p2sh_script_pub_key()


def build_refund_script(sig, public_key, redeem_script):
    return [sig, public_key, 'OP_0', redeem_script.to_hex()]


def build_withdraw_script(sig, public_key, secret, redeem_script):
    return [sig, public_key, secret, 'OP_1', redeem_script.to_hex()]


def extract_secret(tx, input_index, secret_hash: str):
    txin = tx.inputs[input_index]
    secret_pushed_hex = txin.script_sig.get_script()[2]
    secret_pushed = Secret.from_hex(secret_pushed_hex)
    if secret_pushed.secret_hash_hex() != secret_hash:
        raise ValueError('Secret Hash is invalid!')
    return secret_pushed


def jsonify_htlc(htlc, tx_id, file_name):
    dct = {
        "network": htlc.network,
        "secret hash": htlc.secret_hash,
        "end time": htlc.end_time,
        "transaction id": tx_id,
    }
    j = json.dumps(dct, indent=4)
    filename = file_name + '.json'
    with open(filename, "w") as json_file:
        json_file.write(j)