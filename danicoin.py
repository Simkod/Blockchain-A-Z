
"""
Created on Tue Jul  5 22:35:09 2022
@Module 1 - Create a Cryptocurrency

@author: sida
"""

import datetime
import hashlib
import json
import requests

from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse

# Part 1 - Building a Blockchain

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        self.proof_complexity = 3

    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash
                 }
        
        self.chain.append(block)
        return block
        
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            check_proof = self.check_leading_zeros(hash_operation)
            if check_proof == False:
                new_proof += 1
        return new_proof
            
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def is_chain_valid(self):
        chain = self.chain
        previous_block = chain[0]
        block_index = 1;
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if(self.check_leading_zeros(hash_operation) == False):
                return False
            previous_block = block
            block_index += 1
        return True
    
    def check_leading_zeros(self, hash):
        for character in hash[:self.proof_complexity]:
            if character != '0':
                return False
        return True
             
# Part 2 - Mining blockchain

# Creating a Web App
app = Flask(__name__)

blockchain = Blockchain()

#Mining a new Block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'New block successfully mined',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']
                }
    return jsonify(response), 200
    
#Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'lenght' : len(blockchain.chain) 
                }
    return jsonify(response), 200

#Check if chain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    response = {'valid' : blockchain.is_chain_valid()}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)
