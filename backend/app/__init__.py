from flask import Flask, jsonify, request

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

import os
import random
import backend.env
import requests

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub=PubSub(blockchain,transaction_pool)

@app.route('/')
def default_route():
  return 'Welcome to faltu coin'

@app.route('/blockchain')
def blockchain_route():
  return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def mining_route():

  transaction_data = transaction_pool.transaction_data()
  transaction_data.append(Transaction.reward_transaction(wallet).to_json())

  blockchain.add_block(transaction_data)
  
  block=blockchain.chain[-1]
  pubsub.broadcast_block(block)
  transaction_pool.clear_blockchain_transactions(blockchain)

  return jsonify(block.to_json())

@app.route('/wallet/transact',methods=['POST'])
def wallet_transaction_route():
  transaction_data = request.get_json()
  transaction = transaction_pool.existing_transaction(wallet.address)

  if transaction:
    transaction.update(wallet,transaction_data['recipient'],transaction_data['amount'])
  else:
    transaction = Transaction(wallet,transaction_data['recipient'],transaction_data['amount'])

  pubsub.broadcast_transaction(transaction)

  return jsonify(transaction.to_json())

@app.route('/wallet/info')
def wallet_info_route():
  return jsonify({'address':wallet.address,'balance':wallet.balance})

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