
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
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        self.proof_complexity = 3 #Number of leading zeros in hash operation

    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash,
                 'transactions' : self.transactions
                 }
        self.transactions = []
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
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender' : sender,
                                  'receiver' : receiver,
                                  'amount' : amount
                                  })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def check_leading_zeros(self, hash):
        for character in hash[:self.proof_complexity]:
            if character != '0':
                return False
        return True
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_lenght = len(self.chain)
        for node in network:
            response = requests.get(f'http://(node)/get_chain')
            if response.status_code == 200:
                lenght = response.json()['lenght']
                chain = response.json()['chain']
                if lenght > max_lenght and self.is_chain_valid(chain):
                    max_lenght = lenght
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
        
            
# Part 2 - Mining blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-','')

blockchain = Blockchain()

#Mining a new Block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Dani', amount = 10)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'New block successfully mined',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transactions' : block['transactions']
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

#Decentralising the Blockchain

app.run(host = '0.0.0.0', port = 5000)
