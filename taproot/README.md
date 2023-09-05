# Taproot

Here, we have provided three examples using transactions with SegWit version 1, also known as Taproot. It is worth mentioning that in the _Taproot transaction_ and _Taproot 1 of 2 MuSig_ examples, we used the [Bitcoin-utils](https://github.com/karask/python-bitcoin-utils/tree/master/examples)
library, and for the example _Taproot 2 of 3 MuSig_, we used the library available at [taproot workshop repository](https://github.com/bitcoinops/taproot-workshop).
We have directly added this codes to our code and used it for 2 of 2 multisig.

### Taproot Transaction

In this example, we have used an UTXO (unspent transaction output) in the p2tr format, and by providing the appropriate signature (for offline signing, we need the transaction amounts and scriptPubKey) and placing it in the witness, we have spent the bitcoins from the key path. To create transaction output, we have used only one script, which is p2pk.
(see [BIP341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) for more technical details)

Transaction ID:

[348f577ae2509b3b73ebd810c3cdcb18045ef62b43378aed283b3259afe493b1](https://blockstream.info/testnet/tx/348f577ae2509b3b73ebd810c3cdcb18045ef62b43378aed283b3259afe493b1)
### Taproot 1-of-2 MuSig
In this example, we have created a 1of2 multisig using the taproot tree. The leaves of this tree are actually 1of1 multisig scripts or essentially p2pk scripts. Therefore, to spend this transaction, it is sufficient to use one of the public keys to determine the spending path. The rest of the details are similar to the previous example.

Transaction ID:

[808ec85db7b005f1292cea744b24e9d72ba4695e065e2d968ca17744b5c5c14d](https://blockstream.info/testnet/tx/808ec85db7b005f1292cea744b24e9d72ba4695e065e2d968ca17744b5c5c14d)
### Taproot 2-of-3 MuSig
In this example, we are creating a 2of3 multisig that is identified as Musig in the taproot update. To construct the taproot tree, we create three scripts using 2of2 Musig and place them at the leaves of the tree for use from its root. To create an n-of-n Musig, we leverage the special property of Schnorr signatures, namely their linearity. This means that we can add the public keys together to achieve public key aggregation. Later, we can also derive the equivalent private key from the aggregation (for detailed information, you can refer to [BIP340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki)).

After using the [Taproot Workshop](https://github.com/bitcoinops/taproot-workshop) library for public key aggregation, it's sufficient to create three p2pk scripts, and the rest of the process is similar to the previous examples.

Transaction ID:

[3b03b271f0e72f677f308900919f19985881ea6d43f16d5389a560c228ef4a9d](https://blockstream.info/testnet/tx/3b03b271f0e72f677f308900919f19985881ea6d43f16d5389a560c228ef4a9d)