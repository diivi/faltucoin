import uuid
import time

from backend.wallet.wallet import Wallet

from backend.config import MINING_REWARD
from backend.config import MINING_REWARD_INPUT

class Transaction():
  """
  Document the exchange of currency between a sender and one or more recipients.
  """
  def __init__(self, sender_wallet=None, recipient=None, amount=None,id=None, output=None, input=None):
    self.id = id or  str(uuid.uuid4())[0:8]
    self.output = output or  self.create_output(
      sender_wallet,
      recipient,
      amount
    )
    self.input = input or  self.create_input(sender_wallet,self.output)

  def create_output(self,sender_wallet,recipient,amount):
    """
    structure the output data for a transaction
    """
    if amount > sender_wallet.balance:
      raise Exception('Amount exceeds balance!')

    output = {}
    output[recipient] = amount
    output[sender_wallet.address] = sender_wallet.balance - amount
    
    return output

  def create_input(self, sender_wallet, output):
    """
    structure the input data for a transaction
    sign the transaction and include the sender's public key and address 
    """
    return {
      'timestamp': time.time_ns(),
      'amount': sender_wallet.balance,
      'address': sender_wallet.address,
      'public_key': sender_wallet.public_key,
      'signature': sender_wallet.sign(output)
    }

  def update(self, sender_wallet, recipient, amount):
    """
    Update the transaction with a new amount or recipient
    """
    if amount > self.output[sender_wallet.address]:
      raise Exception('Amount exceeds balance!')

    if recipient in self.output:
      self.output[recipient] += amount
    else:
      self.output[recipient]= amount

    self.output[sender_wallet.address] -= amount
    
    self.input= self.create_input(sender_wallet,self.output)

  def to_json(self):
    return self.__dict__
  
  @staticmethod
  def from_json(transaction_json):
    """
    Deserialize transaction json repr back to a Transaction() instance
    """
    return Transaction(**transaction_json)

  @staticmethod
  def is_valid_transaction(transaction):
    """
    validate transactions and raise an exception for invalid ones
    """
    output_total=sum(transaction.output.values())
    
    if transaction.input['amount'] != output_total:
      raise Exception('Invalid Transaction output values!')
     
    if not Wallet.verify(
      transaction.input['public_key'],
      transaction.output,
      transaction.input['signature']
    ):
      raise Exception('Invalid signature')

  @staticmethod
  def reward_transaction(miner_wallet):
    """
    Generate a reward transaction that awards the miner
    """
    output = []
    output[miner_wallet.address] = MINING_REWARD
    
    return Transaction(input = MINING_REWARD_INPUT,output=output)

def main():
  transaction = Transaction(Wallet(), 'recipient', 15)
  print(f'transaction.__dict__: {transaction.__dict__}')

if __name__ == '__main__':
  main()
  
    