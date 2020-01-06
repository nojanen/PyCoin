#!/usr/bin/env python

import logging

from chain import Chain
from block import Block
from wallet import Wallet

def main():

    logging.basicConfig(level=logging.DEBUG)

    UTXOs = {} # Unspend transaction outputs, used by wallets and transactions
    c = Chain()

    w1 = Wallet(UTXOs)
    w2 = Wallet(UTXOs)

    # Make the 1st transaction and generate all coins in the blockchain

    genesis_block = Block()
    genesis_transaction = w1.send_funds(w1.address, 100)
    genesis_block.add_transaction(genesis_transaction)
    c.add_block(genesis_block)

    # Let's spend some coins

    b2 = Block()
    b2.add_transaction(w1.send_funds(w2.address, 1))
    b2.add_transaction(w1.send_funds(w2.address, 2))
    c.add_block(b2)

    # Mine a block just for fun

    c.add_block(Block())

    # Content of the blockchain

    c.print()

    print('Chain is valid:', c.is_valid())

    print('w1 balance:', w1.balance)
    print('w2 balance:', w2.balance)


if __name__ == '__main__':
    main()