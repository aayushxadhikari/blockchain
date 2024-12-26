import hashlib
from textwrap import dedent
import json
from time import time
from uuid import uuid4

from flask import Flask


class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        #Creating the genesis block
        self.new_block(previous_hash = 1, proof = 100)

    def new_block(self, proof, previous_hash=None):

        """
        Create a new block in the blockchain
        :param proof: <int> The proof given by the proof of work algorithm
        :param previous_hash: <Str>  Hash of previous block   
        : return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': self.hash(self.chain[-1]),
        }
        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recepient, amount):
        # Adds a new transaction to the list of transactions
        """
        Create a new transaction to go into the next mined Block
        :para sender <str> address of the sender
        :para recipient <str> address of the receipient
        :para amount: <int> Amount
        :return: <int> The index of the Block that will hold this Transaction
        
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recepient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last block in the chain
        return self.chain[-1]
    
    def proof_of_work(self, last_proof):
        """
        Simple proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains leading 4 0's, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
#instantiate our Node

app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

#istantiate the Blockchain

