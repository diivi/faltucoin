from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
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
    blockchain.add_block(i)
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
