import time
from backend.util.hashing import crypto_hash
from backend.util.hex2bin import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
  'timestamp': 1,
  'last_hash': 'zero',
  'hash': 'genesis_hash',
  'data': [],
  'difficulty': 3,
  'nonce':'genesis_nonce'
} 

class Block:
  """
  A unit of storage in a blockchain
  stores transaction related data
  """
  def __init__(self,timestamp,last_hash,hash,data,difficulty,nonce):
    self.timestamp = timestamp
    self.last_hash = last_hash
    self.hash=hash
    self.data = data
    self.difficulty=difficulty
    self.nonce=nonce
    

  def __repr__(self):
    return (
      'Block('
      f'timestamp: {self.timestamp}, '
      f'last_hash: {self.last_hash}, '
      f'hash: {self.hash}, '
      f'data : {self.data}, '
      f'difficulty:{self.difficulty}, '
      f'nonce:{self.nonce})'
    )
  
  def __eq__(self,other):
    return self.__dict__==other.__dict__

  def to_json(self):
    """
    Serialize the block into a dictionary of its attr
    """
    return self.__dict__


  @staticmethod
  def mine_block(last_block, data):
    """
    create block based on given data until it has the same number of leading zeros as the difficulty 
    """
    timestamp = time.time_ns()
    last_hash = last_block.hash
    difficulty = Block.adjust_difficulty(last_block,timestamp)
    nonce=0
    hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

    while hex_to_binary(hash)[:difficulty] != '0' * difficulty:
      nonce += 1
      timestamp = time.time_ns()
      difficulty = Block.adjust_difficulty(last_block,timestamp)
      hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

    return Block(timestamp,last_hash,hash,data,difficulty,nonce)

  @staticmethod
  def genesis():
    """
    Generating the genesis block
    """
    # return Block(
    #   GENESIS_DATA['timestamp'],
    #   GENESIS_DATA['last_hash'],
    #   GENESIS_DATA['hash'],
    #   GENESIS_DATA['data'],
    # )
    return Block(**GENESIS_DATA)

  @staticmethod
  def from_json(block_json):
    """
    Deserialise a block from its json representation back to a block instance.
    """
    return Block(**block_json)

  @staticmethod
  def adjust_difficulty(last_block,new_timestamp):
    """
    calculate adjusted difficulty acc to mine rate and adjust difficulty accoridingly
    """
    if (new_timestamp - last_block.timestamp) < MINE_RATE:
      return last_block.difficulty+1
    else:
      return last_block.difficulty - 1 if (last_block.difficulty>1) else 1
  @staticmethod
  def is_valid_block(last_block,block):
    """
    Validate block against following rules:
      - must have porper last_hash reference
      - must meet PoW requirement
      - difficulty must only be changed by 1 unit
      - hash must be a valid combination of the block fields 
    """
    if block.last_hash != last_block.hash:
      raise Exception("The block's last_hash is invalid!")

    if hex_to_binary(block.hash)[:block.difficulty] != '0' * block.difficulty:
      raise Exception("The PoW requirement was not met!")

    if abs(last_block.difficulty - block.difficulty) > 1:
      raise Exception("The block difficulty must only adjust by 1!")

    reconstructed_hash = crypto_hash(
      block.timestamp,
      block.last_hash,
      block.data,
      block.difficulty,
      block.nonce
    )
    if block.hash != reconstructed_hash:
      raise Exception("The block hash is incorrect!")

def main():
  genesis_block=Block.genesis()
  good_block = Block.mine_block(Block.genesis(), 'foo')
  # bad_block.last_hash = 'bad_hash'
  try:
    Block.is_valid_block(genesis_block,good_block) 
  except Exception as e:
    print(f'is_valid_block: {e}')
if __name__ == '__main__':
  main()