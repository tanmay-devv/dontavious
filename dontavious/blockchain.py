import json
from datetime import datetime
from hashlib import sha256
import random

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transaction = []

        print("Creating genesis block")
        self.new_block()

    def new_block(self, previous_hash = None):
        block = {
            'index' : len(self.chain),
            'timestamp' : datetime.utcnow().isoformat(),
            'transaction' : self.pending_transaction,
            #'previous_hash' : previous_hash,
            'previous_hash' : self.last_block()['hash'] if self.last_block() else None,
            'nonce' : format(random.getrandbits(64), 'x'),
                }
        block_hash = self.hash(block)
        block['hash'] = block_hash

        self.pending_transaction = []
#        self.chain.append(block)

        print("Mining")
        return block

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    def last_block(self):
        return self.chain[-1] if self.chain else None
    def valid_block(self, block):
        return block['hash'].startswith("0000")

    def proof_of_work(self):
        while True:
            new_block = self.new_block()
            if self.valid_block(new_block):
                break
        self.chain.append(new_block)
        print("Mined a new block successfully", new_block)

