from datetime import datetime

from bitcoinutils.script import Script as BTC_Script
from bitcoinutils.transactions import TxInput as BTC_TxInput, Transaction as BTC_Transaction
from bitcoinutils.utils import to_satoshis as BTC_to_satoshis
from litecoinutils.script import Script as LTC_Script
from litecoinutils.transactions import TxInput as LTC_TxInput, Transaction as LTC_Transaction
from litecoinutils.utils import to_satoshis as LTC_to_satoshis

from htlc import *
from participant import ALICE, CAROL
from secret import Secret

# create HTLC on BTC
ALICE_END_TIME_HTLC = int(datetime.now().timestamp()) + 3600 * 48  # 48 hours later
TX_ID_BTC = 'fb48f4e23bf6ddf606714141ac78c3e921c8c0bebeb7c8abb2c799e9ff96ce6c'
TXOUT_INDEX_BTC = 0
AMOUNT_BTC = 0.09

alice_secret = Secret.from_string('Alice Secret')
alice_htlc = HTLC('btc-test', alice_secret.secret_hash_hex(),
                  ALICE.address, CAROL.address, ALICE_END_TIME_HTLC)

txin_btc = BTC_TxInput(TX_ID_BTC, TXOUT_INDEX_BTC)
txout_btc = alice_htlc.build_fund_utxo(BTC_to_satoshis(AMOUNT_BTC))

alice_tx = BTC_Transaction([txin_btc], [txout_btc])

alice_sig = ALICE.private_key.sign_input(alice_tx, 0, ALICE.address.to_script_pub_key())
txin_btc.script_sig = BTC_Script([alice_sig, ALICE.public_key.to_hex()])

# create HTLC on LTC
CROL_END_TIME_HTLC = int(datetime.now().timestamp()) + 3600 * 24  # 24 hours later
TX_ID_LTC = 'fb48f4e23bf6ddf606714141ac78c3e921c8c0bebeb7c8abb2c799e9ff96ce6c'
TXOUT_INDEX_LTC = 0
AMOUNT_LTC = 1.0

carol_htlc = HTLC('ltc-test', alice_htlc.secret_hash,  # get from HTLC.extract_secret_hash()
                  CAROL.address, ALICE.address, CROL_END_TIME_HTLC)

txin_ltc = LTC_TxInput(TX_ID_LTC, TXOUT_INDEX_LTC)
txout_ltc = carol_htlc.build_fund_utxo(LTC_to_satoshis(AMOUNT_LTC))

carol_tx = LTC_Transaction([txin_ltc], [txout_ltc])

carol_sig = CAROL.private_key.sign_input(carol_tx, 0, CAROL.address.to_script_pub_key())
txin_ltc.script_sig = LTC_Script([carol_sig, CAROL.public_key.to_hex()])

# create swap instance
swap = Swap(alice_htlc, carol_htlc)
print(swap.evaluate())

# Alice creates withdraw trx on LTC

txin = LTC_TxInput(carol_tx.get_txid(), 0)
txout = LTC_TxOutput(LTC_to_satoshis(AMOUNT_LTC), ALICE.address.to_script_pub_key())

alice_withdraw_tx = LTC_Transaction([txin], [txout])

sig = ALICE.private_key.sign_input(alice_withdraw_tx, 0, carol_htlc.script)
txin.script_sig = LTC_Script([alice_secret.secret_hex(), alice_secret.secret_hex(), ALICE.public_key.to_hex(),
                              sig] + carol_htlc.script.script)
print(alice_withdraw_tx)

# Carol creates withdraw trx on BTC

secret = Swap.extract_secret(alice_withdraw_tx, alice_htlc.secret_hash)

txin = BTC_TxInput(alice_tx.get_txid(), 0)
txout = BTC_TxOutput(BTC_to_satoshis(AMOUNT_BTC), CAROL.address.to_script_pub_key())

carol_withdraw_trx = BTC_Transaction([txin], [txout])

sig = CAROL.private_key.sign_input(carol_withdraw_trx, 0, alice_htlc.script)
txin.script_sig = BTC_Script([secret.secret_hex(), secret.secret_hex(), CAROL.public_key.to_hex(),
                              sig] + alice_htlc.script.script)
print(carol_withdraw_trx)
