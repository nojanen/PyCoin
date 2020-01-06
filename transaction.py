#!/usr/bin/env python

import base64
from fastecdsa import keys, curve, ecdsa
from fastecdsa.point import Point
from fastecdsa.encoding.der import DEREncoder
import hashlib
import logging

from transaction_output import TransactionOutput

logger = logging.getLogger('transaction')

class Transaction:

    _sequence = 0
    _curve = curve.secp256k1
    _minimum_transaction = 0.01
    
    def __init__(self, UTXOs, sender: str, recipient: str, value: int, inputs: list):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.transaction_id = self._calculate_hash()
        self.signature = ''
        self.inputs = inputs
        self.recipient_txo = None
        self.leftover_txo = None
        self.UTXOs = UTXOs

    @property
    def data(self):
        return (
            '{self.sender}'
            '{self.recipient}'
            '{self.value}'
        ).format(self=self).encode('utf-8')

    def _calculate_hash(self):
        Transaction._sequence += 1
        return hashlib.sha256((
            '{data}'
            '{sequence}'
        ).format(data=self.data, sequence=Transaction._sequence).encode('utf-8')).hexdigest()

    def add_signature(self, signature):
        self.signature = signature

    def verify(self):
        x, y = DEREncoder.decode_signature(base64.b64decode(self.sender))
        public_key = Point(x, y, Transaction._curve)
        r, s = DEREncoder.decode_signature(base64.b64decode(self.signature))
        return ecdsa.verify((r, s), self.data, public_key, curve=Transaction._curve)

    def process(self):
        if not self.verify():
            logger.warning('Transaction signature failed to verify')
            return False
        
        if self.UTXOs:
            # Normal transaction
            # Map transaction inputs to unspend transaction outputs
            for txi in self.inputs:
                txi.UTXO = self.UTXOs.get(txi.txo_id)

            if self.get_inputs_value() < self.value:
                logger.warning('Inputs less than outputs: %d < %d' % (
                    self.get_inputs_value(), 
                    self.value))
                return False
            
            if self.value < self._minimum_transaction:
                logger.warning('Transaction too small %d' % self.value)
                return False

            leftover = self.get_inputs_value() - self.value
            self.receiver_txo = TransactionOutput(self.recipient, self.value, self.transaction_id)
            self.UTXOs[self.receiver_txo.id] = self.receiver_txo
            
            if leftover > 0:
                self.leftover_txo = TransactionOutput(self.sender, leftover, self.transaction_id)
                self.UTXOs[self.leftover_txo.id] = self.leftover_txo

            for txi in self.inputs:
                if txi.UTXO != None:
                    del self.UTXOs[txi.UTXO.id]
        else:
            # Genesis transaction, we make coins out of nothing
            logger.info('Genesis transactions, we make %d coins out of nothing' % self.value)
            self.receiver_txo = TransactionOutput(self.recipient, self.value, self.transaction_id)
            self.UTXOs[self.receiver_txo.id] = self.receiver_txo

        return True

    @property
    def TXOs(self):
        TXOs = {self.receiver_txo.id: self.receiver_txo}
        if self.leftover_txo:
            TXOs[self.leftover_txo.id] = self.leftover_txo
        return TXOs

    def get_inputs_value(self):
        total = 0
        for txi in self.inputs:
            if txi.UTXO != None:
                total += txi.UTXO.value
        return total

    def get_outputs_value(self):
        total = self.receiver_txo.value
        total += self.leftover_txo.value if self.leftover_txo else 0
        return total

    def __str__(self):
        return (
            'Transaction:\n'
            '  Sender: {self.sender}\n'
            '  Recipient: {self.recipient}\n'
            '  Transaction_id: {self.transaction_id}\n'
            '  Value: {self.value}\n'
            '  Signature: {self.signature}').format(self=self)
