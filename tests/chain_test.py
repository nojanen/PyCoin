#!/usr/bin/env python

import unittest

from chain import Chain
from block import Block
from wallet import Wallet

class ChainTests(unittest.TestCase):

    def setUp(self):
        self.UTXOs = {}
        self.w1 = Wallet(self.UTXOs)
        self.w2 = Wallet(self.UTXOs)

    def _create_genesis_block(self, w):
        b = Block()
        b.add_transaction(w.send_funds(w.address, 10))
        return b

    def test_creation_of_chain(self):
        c = Chain()
        self.assertTrue(c.is_valid())

    def test_add_genesis_block(self):
        b = self._create_genesis_block(self.w1)
        c = Chain()
        c.add_block(b)
        self.assertTrue(c.is_valid())

    def test_many_transaction_in_genesis_block_fails(self):
        b = self._create_genesis_block(self.w1)
        b.add_transaction(self.w1.send_funds(self.w2.address, 1))
        c = Chain()
        c.difficulty = 2
        c.add_block(b)
        self.assertFalse(c.is_valid())


if __name__ == '__main__':
    unittest.main()