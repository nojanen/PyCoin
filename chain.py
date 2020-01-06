#!/usr/bin/env python

import logging

from block import Block

logger = logging.getLogger('chain')

class Chain:
    
    def __init__(self):
        self.blockchain = []
        self.difficulty = 5

    def is_valid(self):
        tmp_UTXOs = {}
        if len(self.blockchain) > 0:
            # Validate genesis block
            block = self.blockchain[0]
            if block.calculate_hash() != block.hash:
                logger.error('Genesis block has invalid hash')
                return False
            if not block.hash.startswith('0' * self.difficulty):
                logger.error('Genesis block is not mined')
                return False
        
            # Validate transactions, only one TX allowed in genesis block
            if len(block.transactions) != 1:
                logger.error('Genesis block has not just one transaction')
                return False
            tx = block.transactions[0]
            if tx.verify() == False:
                logger.error('Invalid transaction in block %d' % i)
                return False
            tmp_UTXOs.update(tx.TXOs)

        for i, block in enumerate(self.blockchain[1:]):
            # Validate block
            if block.calculate_hash() != block.hash:
                logger.error('Invalid hash, block %d' % i+1)
                return False
            if block.previous_hash != self.blockchain[i].hash:
                logger.error('Invalid previous_hash, block %d' % i+1)
                return False
            if not block.hash.startswith('0' * self.difficulty):
                logger.error('Block not mined, block %d' % i+1)
                return False
            if block.merkle_root != block.calculate_merkle_root():
                logger.error('Merkle root not match, block %d' % i+1)
                logger.error('Calculated: %s' % block.calculate_merkle_root())
                logger.error('Was:        %s' % block.merkle_root)
                return False
        
            # Validate transactions
            for tx in block.transactions:
                if tx.verify() == False:
                    logger.error('Invalid transaction in block %d' % i)
                    return False
                if tx.get_inputs_value() != tx.get_outputs_value():
                    logger.error('Inputs are not equal with outputs:\n%s' % tx)
                    return False
                # Validate inputs
                for txi in tx.inputs:
                    if txi.txo_id not in tmp_UTXOs:
                        logger.error('Referenced input is missing\n%s' % txi)
                        return False
                    if txi.UTXO.value != tmp_UTXOs.get(txi.txo_id).value:
                        logger.error('Referenced input value is invalid')
                        return False
                    del tmp_UTXOs[txi.txo_id]

                tmp_UTXOs.update(tx.TXOs)
        return True

    def add_block(self, block: Block):
        if self.blockchain:
            block.mine_block(self.blockchain[-1].hash, self.difficulty)
        else:
            block.mine_block('Genesis Block', self.difficulty)
        self.blockchain.append(block)

    def __str__(self):
        return (
            'Chain:\n'
            '  blocks: {blocks}').format(blocks=len(self.blockchain))

    def print(self):
        print(self)
        for i, block in enumerate(self.blockchain):
            print('Block number', i)
            print(block)
            for tx in block.transactions:
                print(tx)
