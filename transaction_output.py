#!/usr/bin/env python

import hashlib

class TransactionOutput:

    def __init__(self, recipient: str, value: int, parent_transaction_id: str):
        self.recipient = recipient
        self.value = value
        self.parent_transaction_id = parent_transaction_id
        self.id = hashlib.sha256(self.data).hexdigest()

    def is_mine(self, public_key):
        return public_key == self.recipient

    @property
    def data(self):
        return (
            '{self.recipient}'
            '{self.parent_transaction_id}'
            '{self.value}'
        ).format(self=self).encode('utf-8')

    def __str__(self):
        return (
            'TransactionOutput:\n'
            '  recipient: {self.recipient}\n'
            '  value: {self.value}\n'
            '  parent_transaction_id: {self.parent_transaction_id}\n'
            '  id: {self.id}').format(self=self)


# T E S T

def test():
    txo = TransactionOutput('1', 1, '1')
    print(txo)
    print('is_mine:', txo.is_mine('1'))

if __name__ == '__main__':
    test()