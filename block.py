#!/usr/bin/env python

import hashlib
import logging
import time

logger = logging.getLogger('block')

class Block:

    def __init__(self):
        self.previous_hash = ''
        self.timestamp = int(round(time.time() * 1000)) # since 1.1.1970 in milliseconds
        self.transactions = []
        self.merkle_root = ''
        self.hash = ''
        self.nonce = 0

    def add_transaction(self, transaction) -> bool:
        if transaction == None or transaction.process() == False:
            logger.warning('Transaction failed to process. Discarded.')
            return False
        self.transactions.append(transaction)
        return True

    def mine_block(self, previous_hash: str, difficulty: int):
        start_time = time.time() # Just for keeping track how long it takes to mine a block
        self.previous_hash = previous_hash
        self.merkle_root = self.calculate_merkle_root()
        while not self.hash.startswith('0' * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()
        end_time = time.time()
        logger.info('Block mined!: {} (took {} s)'.format(self.hash, round(end_time-start_time, 2)))
        return self

    def calculate_merkle_root(self):
        tree_layer = []
        for t in self.transactions:
            tree_layer.append(t.transaction_id)
        while len(tree_layer) > 1:
            tree_layer = self._calculate_merkle_layer(tree_layer)
        return tree_layer[0] if len(tree_layer) == 1 else "No transactions"

    def _calculate_merkle_layer(self, layer) -> list:
        next_layer = []
        if len(layer) % 2:
            layer.append('')
        for i,j in (layer[i:i+2] for i in range(0, len(layer), 2)):
            next_layer.append(hashlib.sha256('{}{}'.format(i, j).encode('utf-8')).hexdigest())
        return next_layer

    def calculate_hash(self) -> str:
        return hashlib.sha256((
            '{self.previous_hash}'
            '{self.timestamp}'
            '{self.nonce}'
            '{self.merkle_root}'
        ).format(self=self).encode('utf-8')).hexdigest()

    def __str__(self):
        return (
            'Block:\n'
            '  transactions: {transactions}\n'
            '  merkle root: {self.merkle_root}\n'
            '  previous_hash: {self.previous_hash}\n'
            '  timestamp: {self.timestamp}\n'
            '  hash: {self.hash}\n'
            '  nonce: {self.nonce}').format(self=self, transactions=len(self.transactions))
