from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS
import time

blockchain = Blockchain()

times = []

for i in range(1000):
  start = time.time_ns()
  blockchain.add_block(i)
  end = time.time_ns()

  times.append((end - start) / SECONDS)
  average_time = sum(times)/len(times)

  print(f'New block difficulty : {blockchain.chain[-1].difficulty}')
  print(f'Time to mine block : {(end - start) / SECONDS}s')
  print(f'Average time to add blocks: {average_time}s\n')
