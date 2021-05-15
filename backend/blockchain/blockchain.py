from backend.blockchain.block import Block

class Blockchain:
  """
  A public distributed ledger of transactions
  Implemented as a list of blocks (data sets of transactions)
  """
  def __init__(self):
    self.chain=[Block.genesis()]
 
  def add_block(self, data):
    self.chain.append(Block.mine_block(self.chain[-1],data))

  def __repr__(self):
    return f'Blockchain : {self.chain}'

  def replace_chain(self, chain):
    """
    Replace local chain with incoming one when :
      - incoming chain longer than the local one
      - incoming chain is formatted properly
    """
    if len(chain) <= len(self.chain):
      raise Exception("Cannot replace! Incoming chain must be longer than the local one!")

    try:
      Blockchain.is_valid_chain(chain)
    except Exception as e:
      raise Exception(f'Cannot replace! Incoming chain is not valid!')
    
    self.chain = chain

  @staticmethod
  def is_valid_chain(chain):
    """
    Validate incoming chain enforcing the following rules:
      - chain must start with the genesis block
      - blocks must be formatted correctly  (is_valid_block)
    """
    if chain[0] != Block.genesis():
      raise Exception("The Genesis block is not valid!")


    for i in range(1, len(chain)):
      block = chain[i]
      last_block = chain[i - 1]
      Block.is_valid_block(last_block,block)


def main():
  blockchain= Blockchain()
  blockchain.add_block('one')
  blockchain.add_block('two')
  print(blockchain)


if __name__ == '__main__':
  main()