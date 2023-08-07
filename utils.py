from secret import Secret


def build_fund_script(script):
    return script.to_p2sh_script_pub_key()


def build_refund_script(sig, public_key, redeem_script):
    return [sig, public_key, '01'] + redeem_script


def build_withdraw_script(sig, public_key, secret, redeem_script):
    return [sig, public_key, secret, b''] + redeem_script


def extract_secret(tx, secret_hash: str, network=None):  # extract from tx hash
    txin = tx.inputs[0]
    secret_pushed_hex = txin.script_sig.get_script()[2]
    secret_pushed = Secret.from_hex(secret_pushed_hex)
    if secret_pushed.secret_hash_hex() != secret_hash:
        raise ValueError('Secret Hash is invalid!')
    return secret_pushed
