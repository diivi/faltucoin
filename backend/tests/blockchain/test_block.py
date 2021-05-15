from backend.blockchain.block import Block, GENESIS_DATA
from backend.util.hex2bin import hex_to_binary
from backend.config import MINE_RATE, SECONDS
import pytest

import time

def test_mine_block():
  last_block = Block.genesis()
  data = 'test-data'
  block = Block.mine_block(last_block, data)
  
  assert isinstance(block, Block)
  assert block.data == data
  assert block.last_hash == last_block.hash
  assert hex_to_binary(block.hash)[0:block.difficulty]=='0'*block.difficulty

def test_genesis():
  genesis = Block.genesis()
  
  assert isinstance(genesis, Block) 
  for key, value in GENESIS_DATA.items():
    getattr(genesis, key) == value
    
def test_quickly_mined_block():
  last_block = Block.mine_block(Block.genesis(),'foo')
  mined_block = Block.mine_block(last_block,'bar')

  assert mined_block.difficulty==last_block.difficulty+1 #because the blocks are mined consecutively, they were definitely quickly mined  
  
def test_slowly_mined_block():
  last_block = Block.mine_block(Block.genesis(), 'foo')
  time.sleep(MINE_RATE/SECONDS)
  mined_block = Block.mine_block(last_block,'bar')
  
  assert mined_block.difficulty==last_block.difficulty-1 #because of the 4 second delay  
  
def test_lowest_mining_difficulty():
  last_block = Block(
    time.time_ns(),
    'test-last_hash',
    'test-hash',
    'test-data',
    1,
    0
  )

  time.sleep(MINE_RATE/SECONDS)
  mined_block = Block.mine_block(last_block,'bar')

  assert mined_block.difficulty == 1  #ensure that it isnt lower than 1

@pytest.fixture
def last_block():
  return Block.genesis()

@pytest.fixture
def block(last_block):
  return Block.mine_block(last_block,'test-data')

def test_is_valid_block(last_block,block):
  Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_last_hash(last_block,block):
  block.last_hash='bad_last_hash'
  
  with pytest.raises(Exception,match="The block's last_hash is invalid!"):
    Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_pow(last_block,block):
  block.hash = 'abcd'

  with pytest.raises(Exception,match="The PoW requirement was not met!"):
    Block.is_valid_block(last_block, block)

def test_is_valid_block_skipped_difficulty(last_block,block):
  block.difficulty = 10
  block.hash=f'{"0"*block.difficulty}abcd'

  with pytest.raises(Exception,match="The block difficulty must only adjust by 1!"):
    Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_block_hash(last_block,block):
  block.hash = '00000000000000000abcd'
  

  with pytest.raises(Exception,match="The block hash is incorrect!"):
    Block.is_valid_block(last_block, block)
