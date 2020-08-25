from chain import *

class Node:
  def __init__(self):
    self.chain = Chain()
    self.is_selfish = False

  def init_block(self, block):
    block.parent = self.chain.last
    block.height = self.chain.last.height + 1
    return block

  def broadcast(self, block, nodes):
    for node in nodes:
      node.get_block(block)

  def get_block(self, block):
    self.chain.add(block)


class SelfishNode(Node):
  def __init__(self):
    super().__init__()
    self.local_chain = Chain()
    self.is_selfish = True
    self.num_forward_blocks = 0

  def init_block(self, block):
    if self.num_forward_blocks == 0:
      return super().init_block(block)
    else:
      block.parent = self.local_chain.last
      block.height = self.local_chain.last.height + 1
      return block

  def broadcast(self, block):
    # ブロックを広告せずに貯める
    self.local_chain.add(block)
    self.num_forward_blocks += 1

  def genuinely_broadcast(self, block):
    for node in self.nodes:
      node.get_block(block)

  def get_block(self, block):
    super().get_block(block)

    # セルフィッシュマイナーが1個か2個リードしているなら総て広告
    if self.num_forward_blocks in [1, 2]:
      for b in self.local_chain[1:]:
        super().broadcast(b)
      self.num_forward_blocks = 0
      del self.local_chain[1:]

    # 3個以上リードしているなら一つだけ広告
    elif self.num_forward_blocks > 2:
      super().broadcast(self.num_forward_blocks.pop(1))
      self.num_forward_blocks -= 1
