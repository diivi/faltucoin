from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction

from backend.config import STARTING_BALANCE

def test_verify_valid_signature():
  data = {'foo': 'bar'}
  wallet = Wallet()
  signature = wallet.sign(data)

  assert Wallet.verify(wallet.public_key, data, signature)
  
def test_verify_valid_signature():
  data = {'foo': 'bar'}
  wallet = Wallet()
  signature = wallet.sign(data)

  assert not Wallet.verify(Wallet().public_key, data, signature)

def test_calculate_balance():
  blockchain = Blockchain()
  wallet = Wallet()

  assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE
  
  amount = 50
  transaction = Transaction(wallet, 'recipient', amount)
  blockchain.add_block([transaction.to_json()])

  assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount
  
  received_amount_1 = 25
  recieved_transaction_1 = Transaction(
    Wallet(),
    wallet.address,
    received_amount_1
  )

  received_amount_2 = 100
  recieved_transaction_2 = Transaction(
    Wallet(),
    wallet.address,
    received_amount_2
  )

  blockchain.add_block([recieved_transaction_1.to_json(),recieved_transaction_2.to_json()])

  assert Wallet.calculate_balance(blockchain,wallet.address) == STARTING_BALANCE - amount + received_amount_1+received_amount_2