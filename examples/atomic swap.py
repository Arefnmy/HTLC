from datetime import datetime

from bitcoinutils.script import Script as BTC_Script
from bitcoinutils.transactions import TxInput as BTC_TxInput, Transaction as BTC_Transaction, TxOutput as BTC_TxOutput
from bitcoinutils.utils import to_satoshis as BTC_to_satoshis
from litecoinutils.script import Script as LTC_Script
from litecoinutils.transactions import TxInput as LTC_TxInput, Transaction as LTC_Transaction, TxOutput as LTC_TxOutput
from litecoinutils.utils import to_satoshis as LTC_to_satoshis

from htlc import HTLC, Swap
from participant import ALICE, CAROL
from secret import Secret
from utils import build_fund_script, extract_secret, build_withdraw_script

# Alice creates HTLC on BTC
ALICE_END_TIME_HTLC = int(datetime.now().timestamp()) + 3600 * 48  # 48 hours later
TX_ID_BTC = '81bee81bbb08606c812e1fdda9e883fe72b2e73d3c723fc79c60906dc93e2b70'
TXOUT_INDEX_BTC = 0
AMOUNT_BTC = 0.09

alice_secret = Secret.from_string('Alice Secret')
print('Alice Secret Hex : ', alice_secret.secret_hex())

alice_htlc = HTLC('btc-test', alice_secret.secret_hash_hex(),
                  ALICE.address, CAROL.address, ALICE_END_TIME_HTLC)

txin_btc = BTC_TxInput(TX_ID_BTC, TXOUT_INDEX_BTC)
txout_btc = BTC_TxOutput(BTC_to_satoshis(AMOUNT_BTC), build_fund_script(alice_htlc.script))

alice_fund_tx = BTC_Transaction([txin_btc], [txout_btc])

alice_sig = ALICE.private_key.sign_input(alice_fund_tx, 0, ALICE.address.to_script_pub_key())
txin_btc.script_sig = BTC_Script([alice_sig, ALICE.public_key.to_hex()])

print('Alice Fund Transaction ID : ', alice_fund_tx.get_txid())
print('Alice Fund Transaction : \n', alice_fund_tx)

# Carol creates HTLC on LTC
CAROL_END_TIME_HTLC = int(datetime.now().timestamp()) + 3600 * 24  # 24 hours later
TX_ID_LTC = '03964e682cbf0998ecff4eb2ae203ffb5fdeeabe4eb7345c9e55aa9aad48687d'
TXOUT_INDEX_LTC = 0
AMOUNT_LTC = 1.0

carol_htlc = HTLC('ltc-test', alice_secret.secret_hash_hex(),  # Carol has alice secret
                  CAROL.address, ALICE.address, CAROL_END_TIME_HTLC)

txin_ltc = LTC_TxInput(TX_ID_LTC, TXOUT_INDEX_LTC)
txout_ltc = LTC_TxOutput(LTC_to_satoshis(AMOUNT_LTC), build_fund_script(carol_htlc.script))

carol_fund_tx = LTC_Transaction([txin_ltc], [txout_ltc])

carol_sig = CAROL.private_key.sign_input(carol_fund_tx, 0, CAROL.address.to_script_pub_key())
txin_ltc.script_sig = LTC_Script([carol_sig, CAROL.public_key.to_hex()])

print('Carol Fund Transaction ID : ', carol_fund_tx.get_txid())
print('Carol Fund Transaction : \n', carol_fund_tx)

# create swap instance
swap = Swap(alice_htlc, carol_htlc)
print('Swap terms are valid : ', swap.evaluate())

# Alice creates withdraw trx on LTC

txin = LTC_TxInput(carol_fund_tx.get_txid(), 0)  # Alice has Carol's fund transaction id
txout = LTC_TxOutput(LTC_to_satoshis(AMOUNT_LTC), ALICE.address.to_script_pub_key())

alice_withdraw_tx = LTC_Transaction([txin], [txout])

sig = ALICE.private_key.sign_input(alice_withdraw_tx, 0, carol_htlc.script)  # Alice has redeem_script to unlock
txin.script_sig = LTC_Script(build_withdraw_script(sig, ALICE.public_key.to_hex(), alice_secret.secret_hex(),
                                                   carol_htlc.script))
print('Alice Withdraw Transaction ID : ', alice_withdraw_tx.get_txid())
print('Alice Withdraw Transaction : \n', alice_withdraw_tx)

# Carol creates withdraw trx on BTC

secret = extract_secret(alice_withdraw_tx, alice_htlc.secret_hash)
print('Secret Hex Extracted : ', secret.secret_hex())

txin = BTC_TxInput(alice_fund_tx.get_txid(), 0)  # Carol has Alice's fund transaction id
txout = BTC_TxOutput(BTC_to_satoshis(AMOUNT_BTC), CAROL.address.to_script_pub_key())

carol_withdraw_trx = BTC_Transaction([txin], [txout])

sig = CAROL.private_key.sign_input(carol_withdraw_trx, 0, alice_htlc.script)
txin.script_sig = BTC_Script(build_withdraw_script(sig, CAROL.public_key.to_hex(), secret.secret_hex(),
                                                   alice_htlc.script))
print('Carol Withdraw Transaction ID : ', carol_withdraw_trx.get_txid())
print('Carol Withdraw Transaction : \n', carol_withdraw_trx)
