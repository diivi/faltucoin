from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_add_transaction():
  transaction_pool = TransactionPool()
  transaction = Transaction(Wallet(), 'recipient', 1)
  transaction_pool.add_transaction(transaction)

  assert transaction_pool.transaction_map[transaction.id] ==transaction