import random
from chain import *

class Node:
  def __init__(self, gamma, is_selfish):
    self.chain = Chain()
    self.is_selfish = is_selfish
    self.gamma = gamma

  def __del__(self):
    del self.chain

  def init_block(self, block):
    block.parent = self.chain.last
    block.height = self.chain.last.height + 1
    return block

  def broadcast(self, block, nodes):
    for node in nodes:
      node.get_block(block, nodes)

  def get_block(self, block, nodes):
    self.chain.add(block)

  def get_block_called_by_selfish(self, block, nodes):
    self.chain.add(block)
    if self.chain.last.height == block.height and random.random() < self.gamma:
      self.chain.last = block

  def broadcast_all_left(self, nodes):
    pass


class SelfishNode(Node):
  def __init__(self, gamma, is_selfish=True):
    super().__init__(gamma, is_selfish)
    self.local_chain = Chain()
    self.num_forward_blocks = 0
    self.tip_is_selfish = True

  def __del__(self):
    del self.chain
    del self.local_chain

  def init_block(self, block):
    if self.tip_is_selfish:
      return super().init_block(block)
    else:
      block.parent = self.local_chain.last
      block.height = self.local_chain.last.height + 1
      return block

  def broadcast(self, block, nodes):
    # 広告する
    self.genuinely_broadcast(block, nodes)

  def genuinely_broadcast(self, block, nodes):
    for node in nodes:
      node.get_block_called_by_selfish(block, nodes)

  def get_block(self, block, nodes):
    self.local_chain.copy(self.chain)
    super().get_block(block, nodes)
    self.tip_is_selfish = False

  def get_block_called_by_selfish(self, block, nodes):
    self.tip_is_selfish = True
    self.chain.add(block)
    self.local_chain.copy(self.chain)
    # chainだと新しいブロックの高さが元のチェーンの高さを超えないとlastを更新しない。selfish由来のブロックならチェーンと同じ高さでも優先する
    if self.chain.last.height == block.height:
      self.chain.last = block

  def broadcast_all_left(self, nodes):
    pass
