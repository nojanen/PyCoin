#!/usr/bin/env python

import unittest

from block import Block

class BlockTests(unittest.TestCase):

    def test_mining_a_block(self):
        b = Block()
        b.mine_block('prev_hash', 2)
        self.assertTrue(b.hash.startswith('00'))

    def test_calculate_various_size_merkle_roots(self):
        class TransactionMock:
            def __init__(self, id):
                self.transaction_id = id
            def process(self):
                return True

        b = Block()
        for i in range(10):
            b.add_transaction(TransactionMock(str(i)))
            b.calculate_merkle_root()
        # Good, no exceptions

if __name__ == '__main__':
    unittest.main()