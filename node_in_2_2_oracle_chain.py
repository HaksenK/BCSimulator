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
    # local_chainに同じ高さのものが既に有ったら受け入れない
    if self.local_chain.last.height < block.height:
      self.num_forward_blocks += 1
      self.local_chain.add(block)

  def genuinely_broadcast(self, block, nodes):
    for node in nodes:
      node.get_block_called_by_selfish(block, nodes)

  def get_block(self, block, nodes):
    self.chain_is_competing = False
    super().get_block(block, nodes)

    # パブリックブランチのheightがプライベートのものと並んだら一気に広告
    if self.chain.last.height == self.local_chain.last.height:
      # local_chain[0]はgenesis block
      for b in self.local_chain[1:]:
        self.genuinely_broadcast(b, nodes)
      self.num_forward_blocks = 0
      del self.local_chain[1:]

  def get_block_called_by_selfish(self, block, nodes):
    self.chain.add(block)
    # chainだと新しいブロックの高さが元のチェーンの高さを超えないとlastを更新しない。selfish由来のブロックならチェーンと同じ高さでも優先する
    if self.chain.last.height == block.height:
      self.chain.last = block

  def broadcast_all_left(self, nodes):
    for b in self.local_chain[1:]:
      self.genuinely_broadcast(b, nodes)
