from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
import os
import random
import backend.env

app = Flask(__name__)
blockchain = Blockchain()
pubsub=PubSub()

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

PORT = 5000

if os.environ.get('PEER')=='True':
  PORT=random.randint(5001,6000)

app.run(port=PORT)