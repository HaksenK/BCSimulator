from chain import *

class Node:
  def __init__(self, num):
    self.chain = Chain()
    self.id = num
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
    self.has_local_chain = False
