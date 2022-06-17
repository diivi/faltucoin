from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

from backend.config import MINING_REWARD_INPUT

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
      raise Exception('Cannot replace! Incoming chain is not valid!')

    self.chain = chain

  def to_json(self):
    """
    Serialize the blockchain into a list of blocks.
    """
    return list(map(lambda block : block.to_json(),self.chain))

  @staticmethod
  def from_json(chain_json):
    """
    Deserialise a list of blocks into a blockchain instance.
    """
    blockchain = Blockchain()
    blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))
    return blockchain

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
      Block.is_valid_block(last_block, block)
    
    Blockchain.is_valid_transaction_chain(chain)

  @staticmethod
  def is_valid_transaction_chain(chain):
    """
    enforce the rules of a chain composed of blocks of transactions
      - each transaction must only appear once in a chain
      - only 1 mining reward per block
      - each transaction must be valid
    """
    transaction_ids=set()
    for i in range(len(chain)):
      block = chain[i]
      has_mining_reward = False
      for transaction_json in block.data:
        transaction = Transaction.from_json(transaction_json)
        if transaction.id in transaction_ids:
          raise Exception(f'Transaction {transaction.id} is not unique!')

        transaction_ids.add(transaction.id)

        if transaction.input == MINING_REWARD_INPUT:
          if has_mining_reward == True:
            raise Exception(
                f'There can only be one mining reward per block! Check block with hash {block.hash}'
            )
          has_mining_reward = True
        else:
          blockchain_history = Blockchain()
          blockchain_history.chain = chain[:i]

          balance_history = Wallet.calculate_balance(blockchain_history,transaction.input['address'])

          if balance_history != transaction.input['amount']:
            raise Exception(f'Transaction {transaction.id} has an invalid input amount!')

          Transaction.is_valid_transaction(transaction)

def main():
  blockchain= Blockchain()
  blockchain.add_block('one')
  blockchain.add_block('two')
  print(blockchain)


if __name__ == '__main__':
  main()