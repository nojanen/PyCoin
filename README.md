# PyCoin

Blockchain with Python.

Inspired by [Kass' blog writing](https://medium.com/programmers-blockchain/create-simple-blockchain-java-tutorial-from-scratch-6eeed3cb03fa).

The first transaction in the first block generates all the coins in the PyCoin. And only one transaction allowed in the 1st block.

# Usage

The first block, the genesis block, can contain only one transaction that creates
all the coins for the blockchain.

See `main.py`.

# Testing

Use `nose`:
```
$ nosetests
```
