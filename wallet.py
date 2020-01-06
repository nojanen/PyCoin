#!/usr/bin/env python
#
# Requires:
# sudo apt install python3-pip
# sudo apt-get install python-dev libgmp3-dev
# pip3 install fastecdsa

import base64
from fastecdsa import keys, curve, ecdsa
from fastecdsa.encoding.der import DEREncoder
import logging

from transaction import Transaction
from transaction_input import TransactionInput

logger = logging.getLogger('wallet')

class Wallet:

    _curve = curve.secp256k1

    def __init__(self, UTXOs):
        self.UTXOs = UTXOs
        self.private_key, self.public_key = keys.gen_keypair(self._curve)

    def _sign_transaction(self, transaction):
        r, s = ecdsa.sign(transaction.data, self.private_key, curve=Wallet._curve)
        signature = base64.b64encode(DEREncoder.encode_signature(r, s))
        transaction.add_signature(signature)

    @property 
    def address(self):
        return base64.b64encode(DEREncoder.encode_signature(
            self.public_key.x, self.public_key.y))

    @property
    def balance(self):
        balance, _ = self._get_my_funds()
        return balance

    def _get_my_funds(self):
        total = 0
        my_UTXOs = []
        my_address = self.address
        for UTXO in self.UTXOs.values():
            if UTXO.is_mine(my_address):
                total += UTXO.value
                my_UTXOs.append(UTXO)
        return total, my_UTXOs

    def _use_my_funds(self, inputs):
        for txi in inputs:
            del self.UTXOs[txi.txo_id]

    def send_funds(self, recipient: str, value: int):
        inputs = []
        if self.UTXOs:
            # Not a genesis transaction, do all necessary balance checks
            balance, my_UTXOs = self._get_my_funds()
            if balance < value:
                logger.warning('Not enough funds to send transaction. Transaction discarded')
                return None

            total = 0
            for utxo in my_UTXOs:
                total += utxo.value
                inputs.append(TransactionInput(utxo.id))
                if total >= value:
                    break
        # else:
        # This is the genesis transaction, make coins out of nothing (i.e. no checking)
        new_transaction = Transaction(self.UTXOs, self.address, recipient, value, inputs)

        self._sign_transaction(new_transaction)

        return new_transaction
        
    def __str__(self):
        return (
            'Wallet:\n'
            '  address: {self.address}\n'
            '  balance: {self.balance}'
        ).format(self=self)
