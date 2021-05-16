from flask import Flask, jsonify, request

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction

import os
import random
import backend.env
import requests

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet()
pubsub=PubSub(blockchain)

@app.route('/')
def default_route():
  return 'Welcome to faltu coin'

@app.route('/blockchain')
def blockchain_route():
  return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def mining_route():
  transaction_data = 'hard_transaction_data'

  blockchain.add_block(transaction_data)
  
  block=blockchain.chain[-1]
  pubsub.broadcast_block(block)

  return jsonify(block.to_json())

@app.route('/wallet/transact',methods=['POST'])
def wallet_transaction_route():
  transaction_data = request.get_json()
  transaction = Transaction(wallet,transaction_data['recipient'],transaction_data['amount'])

  return jsonify(transaction.to_json())

PORT = 5000

if os.environ.get('PEER')=='True':
  PORT = random.randint(5001, 6000)
  
  result = requests.get('http://localhost:5000/blockchain')
  
  result_blockchain = Blockchain.from_json(result.json())

  try:
    blockchain.replace_chain(result_blockchain.chain)
    print('\n -- Successfully synchronized the local chain')
  except Exception as e:
    print(f'\n -- Error synchronizing: {e}')

app.run(port=PORT)