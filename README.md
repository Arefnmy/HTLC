# Atomic Swap 

We have three examples that show how HTLC works with fund, refund, and withdraw transactions. Then in the atomic swap example, we swap two cryptocurrencies namely bitcoin and litecoin with each other.

- fund :

In this example, Alice creates a basic transaction and sends 0.09 BTC to p2sh Bob's address. At first, Alice initialized the HTLC instance with a secret hash and addresses. After that, Alice initializes the transaction instance with one input and one output. (We assume that the remaining BTC are fees!)
Alice then signs the transaction output and puts the hash of the redeem script (That initialized when HTLC initialized) in the scriptSig.

The BIP199 HTLC script:

`OP_IF 
[HASHOP] <secret_hash> OP_EQUALVERIFY OP_DUP OP_HASH160 <recipient_address_hash> OP_EQUALVERIFY OP_CHECKSIG
OP_ELSE
<endtime> [TIMEOUTOP] OP_DROP OP_DUP OP_HASH160 <sender_address_hash> OP_EQUALVERIFY OP_CHECKSIG 
OP_ENDIF`

HASHOP is either OP_SHA256 or OP_HASH160 and
TIMEOUTOP is either OP_CHECKSEQUENCEVERIFY or OP_CHECKLOCKTIMEVERIFY.

Alice uses OP_SHA256 and OP_CHECKLOCKTIMEVERIFY respectively and sets the endtime in timestamps one hour later.

Alice fund transaction :

ID : `d6079f263cec46192f1f139de52229925c39e9eda814d67a1307058e10a06edd`

ScriptPubKey : 
`OP_HASH160, 78158b1108353ec00ba26ea19009dee5877b3c48, OP_EQUAL`
- withdraw : 

After Alice created the fund transaction, Bob had the transaction ID and secret hash so initiate HTLC instance to use that script.  Then Bob creates the transaction with one input and one output that spends the p2sh transaction out Alice created. Bob signs transaction input and puts his signature, public key, 0x01(or OP_1 for executing OP_IF), and secret in scriptSig and adds a redeem script to those.

Bob withdraw transaction:

ID :
`f02a74982066796c797dc23d6da8315db4997b08b29aeaea4f1654fb69f35d84`

ScriptSig :
`304402201fd233041001b7e77544ca49c69400b040ff64c39b8eca91f2e4ea8b0ffb8b4b022078b91ccbafb0ff8560694625b26957811939ff38def0e1aad00363c2b512681001 0304fcd480b97f54cc4dee06bb9457bd03cf04a7178656d50c0297affbbe79c22f
70b02494643d5084471db6ed484ef2332477ecaeb7d465b4fd1d096b11eb6da8 OP_1 OP_IF OP_SHA256 401b46728f451291bd78967e1ed0fd380429179650e9d5c365d0a591fdc85850
OP_EQUALVERIFY OP_DUP OP_HASH160 e4c6ccda88a296d974dd4f0dd2f406f944be3b47
OP_EQUALVERIFY OP_CHECKSIG OP_ELSE 64d0fc04 OP_CHECKLOCKTIMEVERIFY OP_DROP OP_DUP OP_HASH160 4f5099f0182b8b0d6182275c3c9336b15a596129 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF`
- refund :

Suppose that the transaction that Alice created has timed out and Alice wants to refund that. So again Alice initializes the HTLC instance and uses the fund transaction ID to spend that output. According to BIP0065, Alice should put sequences of transaction inputs less than the maximum sequence mean 0xffffffff. so a good choice is 0xfffffffe. The locktime also should be greater than or equal to the end time that had been set in the script. Alice sets the locktime equal to the end time. Then she signs the transaction and puts her signature, public key, empty byte (or OP_FALSE for reject OP_IF and execute OP_ELSE opcode), and redeem script in the scriptSig.

Alice refund transaction :

ID : 
`b6a5dbc3f7a6b81680f46ca6bc8228ade09fb9ce2ce8ddf5127c6f082ef6c594`

ScriptSig :
`304402203cde824761060f6385ba14ec35f767e504d4ae1b877c98164e22f2ba6eb3653c02200700300288c498ad58d97ce21a7a0070a35e8087085e29cc021667204376883001,
02ee13962c2015d5422d9cb0925bfc389c5919d69e675aa2ced02df9b286d43ccd, OP_0, OP_IF, OP_SHA256, 401b46728f451291bd78967e1ed0fd380429179650e9d5c365d0a591fdc85850,
OP_EQUALVERIFY, OP_DUP, OP_HASH160, 27c8bb725a66355a43c853b6dfe60f4f9b1da28b, OP_EQUALVERIFY, OP_CHECKSIG, OP_ELSE, 64d57ef7, OP_CHECKLOCKTIMEVERIFY, OP_DROP,
OP_DUP, OP_HASH160, b3b76419217a47a2b7805542e439ca3cde5e5973, OP_EQUALVERIFY, OP_CHECKSIG, OP_ENDIF`
- atomic swap :

