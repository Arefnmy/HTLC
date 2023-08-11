# Atomic Swap 

We have three examples demonstrating how Hash Time Locked Contracts (HTLCs) work with fund, refund, and withdraw transactions. Additionally, we present an atomic swap example involving the exchange of two cryptocurrencies: Bitcoin and Litecoin.
- **fund** :

In this example, Alice initiates a basic transaction by sending 0.09 BTC to Bob's p2sh address. Initially, Alice initializes the HTLC instance with a secret hash and addresses. Subsequently, she initializes the transaction instance with one input and one output. (Assuming the remaining BTC covers fees.) Alice then signs the transaction output and places the hash of the redeem script (initialized during HTLC initiation) in the scriptSig.

The BIP199 HTLC script:

`OP_IF 
[HASHOP] <secret_hash> OP_EQUALVERIFY OP_DUP OP_HASH160 <recipient_address_hash> OP_EQUALVERIFY OP_CHECKSIG
OP_ELSE
<endtime> [TIMEOUTOP] OP_DROP OP_DUP OP_HASH160 <sender_address_hash> OP_EQUALVERIFY OP_CHECKSIG 
OP_ENDIF`

Here, HASHOP can be either OP_SHA256 or OP_HASH160, and TIMEOUTOP can be either OP_CHECKSEQUENCEVERIFY or OP_CHECKLOCKTIMEVERIFY. Alice uses OP_SHA256 and OP_CHECKLOCKTIMEVERIFY respectively, and setting the endtime one hour later.

Alice's Fund Transaction:

ID : `d6079f263cec46192f1f139de52229925c39e9eda814d67a1307058e10a06edd`

ScriptPubKey : 
`OP_HASH160, 78158b1108353ec00ba26ea19009dee5877b3c48, OP_EQUAL`
- **withdraw** : 

After Alice creates the fund transaction, Bob possesses the transaction ID and secret hash, enabling him to initiate an HTLC instance for the script. Bob then constructs a transaction with one input and one output that spends Alice's created p2sh transaction output. He signs the transaction input and adds his signature, public key, 0x01 (or OP_1 for OP_IF execution), and secret to the scriptSig. A redeem script is also included.

Bob's Withdraw Transaction:

ID :
`f02a74982066796c797dc23d6da8315db4997b08b29aeaea4f1654fb69f35d84`

ScriptSig :

`304402201fd233041001b7e77544ca49c69400b040ff64c39b8eca91f2e4ea8b0ffb8b4b022078b91ccbafb0ff8560694625b26957811939ff38def0e1aad00363c2b512681001 0304fcd480b97f54cc4dee06bb9457bd03cf04a7178656d50c0297affbbe79c22f
70b02494643d5084471db6ed484ef2332477ecaeb7d465b4fd1d096b11eb6da8 OP_1 OP_IF OP_SHA256 401b46728f451291bd78967e1ed0fd380429179650e9d5c365d0a591fdc85850
OP_EQUALVERIFY OP_DUP OP_HASH160 e4c6ccda88a296d974dd4f0dd2f406f944be3b47
OP_EQUALVERIFY OP_CHECKSIG OP_ELSE 64d0fc04 OP_CHECKLOCKTIMEVERIFY OP_DROP OP_DUP OP_HASH160 4f5099f0182b8b0d6182275c3c9336b15a596129 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF`
- **refund** :

Suppose the transaction Alice created has timed out, and she seeks a refund. Alice reinitializes the HTLC instance and utilizes the fund transaction ID to spend the output. According to BIP0065, Alice must set transaction input sequences to values below the maximum (0xffffffff). A suitable choice is 0xfffffffe. The locktime must also be greater than or equal to the endtime specified in the script. Alice sets the locktime equal to the endtime and signs the transaction. She places her signature, public key, an empty byte (or OP_FALSE to reject OP_IF and execute OP_ELSE opcode), and the redeem script in the scriptSig.

Alice's Refund Transaction:

ID : 
`b6a5dbc3f7a6b81680f46ca6bc8228ade09fb9ce2ce8ddf5127c6f082ef6c594`

ScriptSig :

`304402203cde824761060f6385ba14ec35f767e504d4ae1b877c98164e22f2ba6eb3653c02200700300288c498ad58d97ce21a7a0070a35e8087085e29cc021667204376883001,
02ee13962c2015d5422d9cb0925bfc389c5919d69e675aa2ced02df9b286d43ccd, OP_0, OP_IF, OP_SHA256, 401b46728f451291bd78967e1ed0fd380429179650e9d5c365d0a591fdc85850,
OP_EQUALVERIFY, OP_DUP, OP_HASH160, 27c8bb725a66355a43c853b6dfe60f4f9b1da28b, OP_EQUALVERIFY, OP_CHECKSIG, OP_ELSE, 64d57ef7, OP_CHECKLOCKTIMEVERIFY, OP_DROP,
OP_DUP, OP_HASH160, b3b76419217a47a2b7805542e439ca3cde5e5973, OP_EQUALVERIFY, OP_CHECKSIG, OP_ENDIF`
- **atomic swap** :

In this example, Alice wishes to exchange LTC for BTC. Carol desires to swap her LTC for Alice's BTC. Assuming Alice wants to pay 0.01 BTC and receive 3.52 LTC, she starts by considering the secret and initiating an HTLC instance, setting an end time 48 hours later. She then creates a fund transaction on the Bitcoin network similar to the _fund_ example described above.

Alice secret hash :
`401b46728f451291bd78967e1ed0fd380429179650e9d5c365d0a591fdc85850`

Alice fund transaction ID :
`c63a0ee48ef76a51f06c22786b41661a1dceeb8fc84bb2c77712581d3ea61130`

Carol follows suit by creating her own HTLC instance and fund transaction on the Litecoin network, matching Alice's secret hash. However, she sets the end time 24 hours before Alice's to prevent cheating.

Carol fund transaction ID :
`02f4972ceb3d6570750f5f1b553140eeefd712e494a43826e47a21e2bf7b1c84`

By utilizing Alice and Carol's HTLC instances, a Swap instance can be initialized to verify that secret hashes and end times are correctly aligned.

Subsequently, Alice, in possession of the secret, creates a withdraw transaction prior to the end time, similar to the _withdraw_ example.

Alice withdraw transaction ID :
`ecafa38701042ca9f62e731c26efe9f6ae8b6a6197f3e7f2b7114138bc61322b`

After a period, Carol identifies Alice's transaction on the Litecoin network. She extracts the secret from the scriptSig previously pushed by Alice, giving Carol the ability to spend Alice's fund transaction.

Extracted secret (hex format) :
`70b02494643d5084471db6ed484ef2332477ecaeb7d465b4fd1d096b11eb6da8`

Carol then creates her own withdraw transaction, using the extracted secret to spend Alice's fund transaction.

Carol withdraw transaction ID :
`e8e59395b281e34c6280f85fcf0f6519f3fc88cb57acf8b819e94cf9f4f0126c`

Note that by setting a minimum 24-hour difference for the end times, Carol ensures she has sufficient time to spend Alice's fund transaction.
