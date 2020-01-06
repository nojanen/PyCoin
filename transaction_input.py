#!/usr/bin/env python

class TransactionInput:

    def __init__(self, txo_id: str):
        self.txo_id = txo_id
        self.UTXO = None

    def __str__(self):
        return (
            'TransactionInput:\n'
            '  txo_id: {self.txo_id}').format(self=self)
