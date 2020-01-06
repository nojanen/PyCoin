#!/usr/bin/env python

import unittest

from wallet import Wallet

class WalletTests(unittest.TestCase):

    def setUp(self):
        self.UTXOs = {}

    def _generate_wallet_with_coins(self):
        w = Wallet(self.UTXOs)
        genesis_transaction = w.send_funds(w.address, 10)
        self.assertTrue(genesis_transaction.process())
        self.assertTrue(genesis_transaction.verify())
        self.assertEqual(10, w.balance)
        return w

    def test_create_wallet(self):
        w = Wallet(self.UTXOs)

    def test_wallets_have_different_addresses(self):
        w1 = Wallet(self.UTXOs)
        w2 = Wallet(self.UTXOs)
        self.assertNotEqual(w1.address, w2.address)

    def test_transferring_coins(self):
        w1 = self._generate_wallet_with_coins()
        w2 = Wallet(self.UTXOs)
        t = w1.send_funds(w2.address, 3)
        self.assertTrue(t.process())
        self.assertTrue(t.verify())
        self.assertEqual(7, w1.balance)
        self.assertEqual(3, w2.balance)

    def test_send_more_funds_than_balance_fails(self):
        w1 = self._generate_wallet_with_coins()
        w2 = Wallet(self.UTXOs)
        t = w1.send_funds(w2.address, 11)
        self.assertIsNone(t)
        self.assertEqual(10, w1.balance)
        self.assertEqual(0, w2.balance)

    def test_send_less_funds_than_minimum_fails(self):
        w1 = self._generate_wallet_with_coins()
        w2 = Wallet(self.UTXOs)
        t = w1.send_funds(w2.address, 0.005)
        self.assertFalse(t.process())
        self.assertEqual(10, w1.balance)
        self.assertEqual(0, w2.balance)

    def test_sending_multiple_inputs(self):
        w1 = self._generate_wallet_with_coins()
        w2 = Wallet(self.UTXOs)
        # 10 small transactions from w1 -> w2
        for i in range(10):
            t = w1.send_funds(w2.address, 1)
            self.assertTrue(t.process())
            self.assertTrue(t.verify())
        self.assertEqual(0, w1.balance)
        self.assertEqual(10, w2.balance)
        # 1 big transactions from w2 -> w1
        t = w2.send_funds(w1.address, 10)
        self.assertTrue(t.process())
        self.assertTrue(t.verify())
        self.assertEqual(10, w1.balance)
        self.assertEqual(0, w2.balance)

if __name__ == '__main__':
    unittest.main()