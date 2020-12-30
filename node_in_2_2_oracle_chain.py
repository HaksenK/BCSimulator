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
    self.k=0
    self.l=0
    self.chain_is_competing = False

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
    if self.chain_is_competing:
      self.genuinely_broadcast(block, nodes)
      self.chain_is_competing = False
#      print("selfish won")
      self.k = 0
#      print(f"3: k={self.k} l={self.l}")
    # ブロックを広告せずに貯める
    # local_chainに同じ高さのものが既に有ったら受け入れない
    elif self.local_chain.last.height < block.height:
      if self.chain.last.height == block.height:
        # honest blockと同時に発見された場合
        self.k = -1
        self.l = 0
        self.num_forward_blocks = 0
        self.genuinely_broadcast(block, nodes)
        self.chain.last = block
        self.chain_is_competing = True
#        print(f"4: k={self.k} l={self.l}")
      else:
        self.k +=1
#        print(f"2: k={self.k} l={self.l}")
        self.num_forward_blocks += 1
        self.local_chain.add(block)

  def genuinely_broadcast(self, block, nodes):
    for node in nodes:
      node.get_block_called_by_selfish(block, nodes)

  def get_block(self, block, nodes):
    if self.k>0 and block.height == self.chain.last.height+1:
      self.l+=1
    super().get_block(block, nodes)

    if self.chain_is_competing:
      self.chain_is_competing = False
      self.k = 0

    # パブリックブランチのheightがプライベートのものと並んだら一気に広告
    if self.chain.last.height == self.local_chain.last.height:
      self.chain_is_competing = True
      self.k=-1
      self.l=0
      # local_chain[0]はgenesis block
      for b in self.local_chain[1:]:
        self.genuinely_broadcast(b, nodes)
      self.num_forward_blocks = 0
      del self.local_chain[1:]
#    print(f"1: k={self.k} l={self.l}")
#    print(f"num_forward_blocks: {self.num_forward_blocks}")

  def get_block_called_by_selfish(self, block, nodes):
    self.chain.add(block)
    # chainだと新しいブロックの高さが元のチェーンの高さを超えないとlastを更新しない。selfish由来のブロックならチェーンと同じ高さでも優先する
    if self.chain.last.height == block.height:
      self.chain.last = block

  def broadcast_all_left(self, nodes):
#    print("end")
    for b in self.local_chain[1:]:
      self.genuinely_broadcast(b, nodes)
