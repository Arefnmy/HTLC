import requests
from bitcoinutils.transactions import Transaction

# Simple code to broadcast transactions on testnet
URL = 'https://blockstream.info/testnet/api'
PUSH_TX_URL = '/tx'
FETCH_TX_URL = '/tx/{txid}/raw'


def push_tx(tx_hex):
    response = requests.post(URL + PUSH_TX_URL, tx_hex)
    if response.status_code == 200:
        return response.text
    else:
        return {"error": f"HTTP Error: {response.status_code}"}


def fetch_tx(tx_id):
    response = requests.get(URL + FETCH_TX_URL.format(txid=tx_id))
    if response.status_code == 200:
        return Transaction.from_raw(response.content.hex())
    else:
        return None
