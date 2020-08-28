import numpy.random as rd
from chain import *
from node import *

class BitcoinNetworkSimulator:
  def __init__(self, gamma):
   # ネットワーク全体のパラメタ
    self.num_honest_nodes = 50
    self.num_selfish_nodes = 50
#    self.simulation_period = 60 * 24 # minutes
    self.simulation_period = 100 # minutes

    self.honest_node = Node(gamma)
    self.selfish_node = SelfishNode(gamma)
    self.num_generated_blocks = rd.poisson(0.1, self.simulation_period) #1分に0.1ブロック
    self.latest_block_id = 0 # 総てのブロックの中で最新のもの

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
      block_queue.append(block)

    for block in block_queue:
      # 広告はノードにやらせる
      self.node_of_index(block.miner).broadcast(block, [self.honest_node, self.selfish_node])

  def execute_simulation(self):
    # シミュレーションの実行
    for i in self.num_generated_blocks:
      self.generate_block(i)

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
    chain = self.node_of_index(0).chain.blocks
    while(current_block.height > 0):
      if(node_of_index(current_block.miner).is_selfish):
        r_pool += 1
      else:
        r_others += 1
      current_block = current_block.parent
    return r_pool / (r_pool + r_others)

if __name__ == '__main__':
  simulator = BitcoinNetworkSimulator(0.5)
  simulator.execute_simulation()
  simulator.show_all_blocks()
  simulator.show_rewards()
