import hashlib
import json

def crypto_hash(*args):
  """
  Return SHA-256 hash of the given arguments
  """
  stringified_args = sorted(map(lambda x: json.dumps(x),args))

  joined_data = "".join(stringified_args)
  
  return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
  print(f"crypto_hash('one',2,[3]) : {crypto_hash('one',2,[3])}")

if __name__ == '__main__':
  main()