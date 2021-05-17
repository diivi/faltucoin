from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

import time
import os

import backend.env
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

pnconfig = PNConfiguration()
pnconfig.subscribe_key =os.environ.get('SUB_KEY')
pnconfig.publish_key = os.environ.get('PUB_KEY')

CHANNELS = {
  'TEST': 'TEST',
  'BLOCK': 'BLOCK',
  'TRANSACTION':'TRANSACTION'
}

class Listener(SubscribeCallback):
  def __init__(self, blockchain,transaction_pool):
    self.blockchain = blockchain
    self.transaction_pool = transaction_pool

  def message(self, pubnub, message_obj):
    print(f'\n-- Channel: {message_obj.channel} || Message: {message_obj.message}')
    
    if message_obj.channel == CHANNELS['BLOCK']:
      block = Block.from_json(message_obj.message)
      new_chain = self.blockchain.chain[:]
      new_chain.append(block)

      try:
        self.blockchain.replace_chain(new_chain)
        self.transaction_pool.clear_blockchain_transactions(
          self.blockchain
        )
        print('\n -- Successfully replaced the local chain')
      except Exception as e:
        print(f'\n -- Did not replace chain: {e}')

    elif message_obj.channel == CHANNELS['TRANSACTION']:
      transaction = Transaction.from_json(message_obj.message)
      self.transaction_pool.add_transaction(transaction)
      print('\n -- Added new transaction to the transaction pool!')



class PubSub():
  """
  Handles the publish/subscribe layer of the application.
  Provides communication between all the nodes of the blockchain network.
  """
  def __init__(self,blockchain,transaction_pool):
    self.pubnub = PubNub(pnconfig)
    self.pubnub.subscribe().channels(CHANNELS.values()).execute()
    self.pubnub.add_listener(Listener(blockchain,transaction_pool))
  
  def publish(self, channel, message):
    """
    Publish a message to a channel
    """
    self.pubnub.publish().channel(channel).message(message).sync()
  
  def broadcast_block(self, block):
    """
    Broadcast a block object to all nodes
    """
    self.publish(CHANNELS['BLOCK'],block.to_json())

  def broadcast_transaction(self,transaction):
    """
    Broadcast transaction to all nodes
    """
    self.publish(CHANNELS['TRANSACTION'],transaction.to_json())

def main():
  pubsub = PubSub()
  time.sleep(1)
  pubsub.publish(CHANNELS['TEST'],{'foo':'bar'})

if __name__ == '__main__':
  main()