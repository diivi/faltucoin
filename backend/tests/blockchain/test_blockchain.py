from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

import pytest

def test_blockchain_instance():
  blockchain = Blockchain()
  assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
  blockchain = Blockchain()
  data = 'test-data'
  blockchain.add_block(data)

  assert blockchain.chain[-1].data == data

@pytest.fixture
def populated_blockchain():
  blockchain = Blockchain()
  for i in range(3):
    blockchain.add_block([Transaction(Wallet(),'recipient',i).to_json()])
  return blockchain

def test_is_valid_chain(populated_blockchain):
  Blockchain.is_valid_chain(populated_blockchain.chain)

def test_is_valid_chain_bad_genesis(populated_blockchain):
  populated_blockchain.chain[0].hash = 'bad_hash'
  
  with pytest.raises(Exception,match="The Genesis block is not valid!"):
    Blockchain.is_valid_chain(populated_blockchain.chain)

def test_replace_chain(populated_blockchain):
  blockchain = Blockchain()
  blockchain.replace_chain(populated_blockchain.chain)

  assert blockchain.chain == populated_blockchain.chain

def test_replace_chain_not_longer(populated_blockchain):
  blockchain = Blockchain()
  
  with pytest.raises(Exception,match="Cannot replace! Incoming chain must be longer than the local one!"):
    populated_blockchain.replace_chain(blockchain.chain)

def test_replace_chain_invalid(populated_blockchain):
  blockchain = Blockchain()
  populated_blockchain.chain[1].hash = 'bad_hash'

  with pytest.raises(Exception,match='Cannot replace! Incoming chain is not valid!'):
    blockchain.replace_chain(populated_blockchain.chain)

def test_valid_transaction_chain(populated_blockchain):
  Blockchain.is_valid_transaction_chain(populated_blockchain.chain)

def test_valid_transaction_chain_duplicate_transactions(populated_blockchain):
  transaction = Transaction(Wallet(),'recipient',1).to_json()
  populated_blockchain.add_block([transaction, transaction])
  
  with pytest.raises(Exception,match='is not unique!'):
    Blockchain.is_valid_transaction_chain(populated_blockchain.chain)

def test_valid_transaction_chain_multiple_rewards(populated_blockchain):
  reward_1 = Transaction.reward_transaction(Wallet()).to_json()
  reward_2 = Transaction.reward_transaction(Wallet()).to_json()

  populated_blockchain.add_block([reward_1, reward_2])
  
  with pytest.raises(Exception,match='one mining reward per block'):
    Blockchain.is_valid_transaction_chain(populated_blockchain.chain)

def test_valid_transaction_chain_bad_transaction(populated_blockchain):
  bad_transaction = Transaction(Wallet(), 'recipient', 1)
  bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
  populated_blockchain.add_block([bad_transaction.to_json()])
  with pytest.raises(Exception):
    Blockchain.is_valid_transaction_chain(populated_blockchain.chain)
  
def test_is_valid_transaction_chain_bad_balance_history(populated_blockchain):
  wallet = Wallet()
  bad_transaction = Transaction(wallet, 'recipient', 1)
  bad_transaction.output[wallet.address] = 9000
  bad_transaction.input['amount'] = 9001
  bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)

  populated_blockchain.add_block([bad_transaction.to_json()])
  with pytest.raises(Exception,match='invalid input amount'):
    Blockchain.is_valid_transaction_chain(populated_blockchain.chain)