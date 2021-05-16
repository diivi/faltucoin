from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import time
import os
import backend.env
from backend.blockchain.block import Block

pnconfig = PNConfiguration()
pnconfig.subscribe_key =os.environ.get('SUB_KEY')
pnconfig.publish_key = os.environ.get('PUB_KEY')

CHANNELS = {
  'TEST': 'TEST',
  'BLOCK':'BLOCK'
}

class Listener(SubscribeCallback):
  def __init__(self, blockchain):
    self.blockchain = blockchain

  def message(self, pubnub, message_obj):
    print(f'\n-- Channel: {message_obj.channel} || Message: {message_obj.message}')
    
    if message_obj.channel == CHANNELS['BLOCK']:
      block = Block.from_json(message_obj.message)
      new_chain = self.blockchain.chain[:]
      new_chain.append(block)

      print("\n")
      print(new_chain)
      print("\n")
      print(self.blockchain.chain)

      try:
        self.blockchain.replace_chain(new_chain)
        print('\n -- Successfully replaced the local chain')
      except Exception as e:
        print(f'\n -- Did not replace chain: {e}')

class PubSub():
  """
  Handles the publish/subscribe layer of the application.
  Provides communication between all the nodes of the blockchain network.
  """
  def __init__(self,blockchain):
    self.pubnub = PubNub(pnconfig)
    self.pubnub.subscribe().channels(CHANNELS.values()).execute()
    self.pubnub.add_listener(Listener(blockchain))
  
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

def main():
  pubsub = PubSub()
  time.sleep(1)
  pubsub.publish(CHANNELS['TEST'],{'foo':'bar'})

if __name__ == '__main__':
  main()