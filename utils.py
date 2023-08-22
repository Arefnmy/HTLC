from secret import Secret


def build_fund_script(script):
    return script.to_p2sh_script_pub_key()


def build_refund_script(sig, public_key, redeem_script):
    return [sig, public_key, b'', redeem_script.to_hex()]


def build_withdraw_script(sig, public_key, secret, redeem_script):
    return [sig, public_key, secret, b'01', redeem_script.to_hex()]


def extract_secret(tx, input_index, secret_hash: str):
    txin = tx.inputs[input_index]
    secret_pushed_hex = txin.script_sig.get_script()[2]
    secret_pushed = Secret.from_hex(secret_pushed_hex)
    if secret_pushed.secret_hash_hex() != secret_hash:
        raise ValueError('Secret Hash is invalid!')
    return secret_pushed
