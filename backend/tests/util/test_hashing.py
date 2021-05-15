from backend.util.hashing import crypto_hash

def test_crypto_hash():
  #create same hash for  arguements in any order
  assert crypto_hash(1, [2], 'three') == crypto_hash('three', 1, [2])
  #check general sha functionality
  assert crypto_hash('divi')=='2a3281f0a12b1f925ff37c37c5dccc95c6733a82dae9317620e917e956bcd1d2'