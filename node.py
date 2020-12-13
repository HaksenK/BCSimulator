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


class SelfishNode(Node):
  def __init__(self, gamma, is_selfish=True):
    super().__init__(gamma, is_selfish)
    self.local_chain = Chain()
    self.num_forward_blocks = 0

  def __del__(self):
    del self.chain
    del self.local_chain

  def init_block(self, block):
    if self.num_forward_blocks == 0:
      return super().init_block(block)
    else:
      block.parent = self.local_chain.last
      block.height = self.local_chain.last.height + 1
      return block

  def broadcast(self, block, nodes):
    # ブロックを広告せずに貯める
    self.local_chain.add(block)
    self.num_forward_blocks += 1

  def genuinely_broadcast(self, block, nodes):
    for node in nodes:
      node.get_block_called_by_selfish(block, nodes)

  def get_block(self, block, nodes):
    super().get_block(block, nodes)

    # セルフィッシュマイナーが1個か2個リードしているなら総て広告
    if self.num_forward_blocks in [1, 2]:
      for b in self.local_chain[1:]:
        self.genuinely_broadcast(b, nodes)
      self.num_forward_blocks = 0
      del self.local_chain[1:]

    # 3個以上リードしているなら一つだけ広告
    elif self.num_forward_blocks > 2:
      self.genuinely_broadcast(self.local_chain.pop(1), nodes)
      self.num_forward_blocks -= 1

  def get_block_called_by_selfish(self, block, nodes):
    self.chain.add(block)
    # chainだと新しいブロックの高さが元のチェーンの高さを超えないとlastを更新しない。selfish由来のブロックならチェーンと同じ高さでも優先する
    if self.chain.last.height == block.height:
      self.chain.last = block
