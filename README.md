# PyCoin

Blockchain with Python.

Inspired by [Kass' blog writing](https://medium.com/programmers-blockchain/create-simple-blockchain-java-tutorial-from-scratch-6eeed3cb03fa).

The first transaction in the first block generates all the coins in the PyCoin. And only one transaction allowed in the 1st block.

# Installation

Install required packages.

Ubuntu:
```
$ sudo apt install python3.8-venv python3.8-dev libgmp3-dev
```

Keep Python environments tidy, use virtual env:
```
$ python3 -m venv venv && source venv/bin/activate
```

Install Python libraries (installation of `fastecdsa` fails if `wheel` is not already installed):
```
$ pip3 install wheel
$ pip3 install -r requirements.txt
```

# Usage

The first block, the genesis block, can contain only one transaction that creates
all the coins for the blockchain.

See `main.py`.

# Testing

Use `nose`:
```
$ nosetests
```
