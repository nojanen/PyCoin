#!/usr/bin/env python

import unittest

from transaction import Transaction

class TransactionTests(unittest.TestCase):

    def setUp(self):
        self.UTXOs = {}

    def test_create_transaction(self):
        t = Transaction(self.UTXOs, 'sender', 'receiver', 1, [])

    def test_two_identical_transaction_has_differene_id(self):
        t1 = Transaction(self.UTXOs, 'sender', 'receiver', 1, [])
        t2 = Transaction(self.UTXOs, 'sender', 'receiver', 1, [])
        self.assertNotEqual(t1.transaction_id, t2.transaction_id)

if __name__ == '__main__':
    unittest.main()