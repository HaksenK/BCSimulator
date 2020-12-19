import numpy.random as rd
from chain import *
#from node import *
from node_in_2_1_oracle_chain import *

class BitcoinNetworkSimulator:
  def __init__(self, selfish_node_constructor, num_honest_nodes, num_selfish_nodes, gamma):
   # ネットワーク全体のパラメタ
    self.num_honest_nodes = num_honest_nodes
    self.num_selfish_nodes = num_selfish_nodes
#    self.simulation_period = 60 * 24 * 180# minutes
    self.simulation_period = 60 * 24 * 30# minutes
#    self.simulation_period = 60 * 24 # minutes
#    self.simulation_period = 200 # minutes

    self.honest_node = Node(gamma, False)
    self.selfish_node = selfish_node_constructor(gamma, True)
    self.latest_block_id = 0 # 総てのブロックの中で最新のもの

  def __del__(self):
    del self.honest_node
    del self.selfish_node

  def node_of_index(self, n):
    # 配列にnum_honest_nodes+num_selfish_nodes個のブロックを入れると、別のインスタンスになっている模様。この函数で擬似的な配列を作る
    if n < self.num_honest_nodes:
      return self.honest_node
    elif n < self.num_honest_nodes + self.num_selfish_nodes:
      return self.selfish_node
    else:
      return None

  def generate_block(self, num_blocks):
    # ブロックをnum_blocks個生成し、生成したマイナーをランダムに決める
    # ブロックをいきなりbroadcastせず、init後にキューに入れる。こうするとブロックのheightが同じになる
    block_queue = []
    for i in range(num_blocks):
      self.latest_block_id += 1
      miner_index = rd.randint(0, self.num_honest_nodes + self.num_selfish_nodes)
      b = Block(self.latest_block_id, miner_index)
      block = self.node_of_index(miner_index).init_block(b)
#      print(block.id)
#      print(block.miner)
#      print(block.parent.id)
#      print(block.height)
#      print("\n")
      block_queue.append(block)
#    if block_queue: print("\n")

    for block in block_queue:
      # 広告はノードにやらせる
      self.node_of_index(block.miner).broadcast(block, [self.honest_node, self.selfish_node])

  def execute_simulation(self):
    # シミュレーションの実行
    for i in rd.poisson(0.1, self.simulation_period): #1分に0.1ブロック
      self.generate_block(i)
    self.selfish_node.broadcast_all_left([self.honest_node, self.selfish_node])

  def show_rewards(self):
    current_block = self.node_of_index(0).chain.last
    rewards = [0] * (self.num_honest_nodes + self.num_selfish_nodes)
    while(current_block.height > 0):
      rewards[current_block.miner] += 1
      current_block = current_block.parent
    for i, reward in enumerate(rewards):
      if self.node_of_index(i).is_selfish:
        print(f'Selfish miner {i}: reward {reward}')
      else:
        print(f'Honest miner {i}: reward {reward}')

  def show_all_blocks(self):
    chain = self.node_of_index(0).chain.blocks
    for b in chain:
      print(f'block id: {b.id}')
      print(f'miner: {b.miner}')
      if b.parent:
        print(f'parent: {b.parent.id}')
      print(f'height: {b.height}')
      print()

  def show_R_pool(self):
    r_pool = 0
    r_others = 0
    current_block = self.node_of_index(0).chain.last
    while(current_block.height > 0):
      if(self.node_of_index(current_block.miner).is_selfish):
        r_pool += 1
      else:
        r_others += 1
      current_block = current_block.parent
    return r_pool / (r_pool + r_others)

if __name__ == '__main__':
  simulator = BitcoinNetworkSimulator(SelfishNode, 10, 10, 0.5)
  simulator.execute_simulation()
  simulator.show_all_blocks()
  simulator.show_rewards()
  print(simulator.show_R_pool())
