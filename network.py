import requests
from bitcoinutils.transactions import Transaction

# Simple code to broadcast transactions on testnet
URL = 'https://blockstream.info/testnet/api'
PUSH_TX_URL = '/tx'
FETCH_TX_URL = '/tx/{txid}/raw'


def push_tx(tx_hex, network='testnet'):
    if network == 'testnet':
        url = URL + PUSH_TX_URL
    else:
        raise NotImplemented
    response = requests.post(url, tx_hex)
    if response.status_code == 200:
        return f'Success: Transaction ID: {response.text}'
    else:
        return response.text


def fetch_tx(tx_id, network='testnet'):
    response = requests.get(URL + FETCH_TX_URL.format(txid=tx_id))
    if response.status_code == 200:
        return Transaction.from_raw(response.content.hex())
    else:
        return None
