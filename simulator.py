import numpy.random as rd
from chain import *
from node import *

class BitcoinNetworkSimulator:
  def __init__(self):
    # ネットワーク全体のパラメタ
    self.num_honest_nodes = 100
    self.num_selfish_nodes = 0
    self.gamma = 0.5
    self.simulation_period = 60 * 24 # minutes

    self.nodes = []
    self.num_generated_blocks = rd.poisson(0.1, self.simulation_period) #1分に0.1ブロック
    self.latest_block_id = 0 # 総てのブロックの中で最新のもの

    for i in range(self.num_honest_nodes):
      self.nodes.append(Node(i))
    for i in range(self.num_selfish_nodes):
      self.nodes.append(SelfishNode(i + self.num_honest_nodes))

  def broadcast(self, block):
    # ブロックを総てのノードに配布する
    for node in self.nodes:
      node.get_block(block)

  def generate_block(self, num_blocks):
    # ブロックをnum_blocks個生成し、生成したマイナーをランダムに決める
    # ブロックをいきなりbroadcastせず、init後にキューに入れる。こうするとブロックのheightが同じになる
    block_queue = []
    for i in range(num_blocks):
      self.latest_block_id += 1
      miner_index = rd.randint(0, self.num_honest_nodes + self.num_selfish_nodes)
      b = Block(self.latest_block_id, miner_index)
      block = self.nodes[miner_index].init_block(b)
      block_queue.append(block)

    for block in block_queue:
      self.broadcast(block)

  def execute_simulation(self):
    # シミュレーションの実行
    for i in self.num_generated_blocks:
      self.generate_block(i)

  def show_rewards(self):
    current_block = self.nodes[0].chain.last
    rewards = [0] * (self.num_honest_nodes + self.num_selfish_nodes)
    while(current_block.height > 0):
      rewards[current_block.miner] += 1
      current_block = current_block.parent
    for i, reward in enumerate(rewards):
      if self.nodes[i].is_selfish:
        print(f'Selfish miner {i}: reward {reward}')
      else:
        print(f'Honest miner {i}: reward {reward}')

  def show_all_blocks(self):
    chain = self.nodes[0].chain.blocks
    for b in chain:
      print(f'block id: {b.id}')
      print(f'miner: {b.miner}')
      if b.parent:
        print(f'parent: {b.parent.id}')
      print(f'height: {b.height}')
      print()


if __name__ == '__main__':
  simulator = BitcoinNetworkSimulator()
  simulator.execute_simulation()
#  simulator.show_all_blocks()
  simulator.show_rewards()
