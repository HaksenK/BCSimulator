import copy

class Block:
  def __init__(self, num, miner):
    self.parent = None
    self.id = num
    self.miner = miner
    self.height = -1

class GenesisBlock(Block):
  def __init__(self):
    self.parent = None
    self.id = 0
    self.miner = -1
    self.height = 0

class Chain:
  def __init__(self):
    self.last = GenesisBlock()
    self.blocks = [self.last]
    self.is_in_competition = False

  def __getitem__(self, x):
    return self.blocks[x]

  def __delitem__(self, val):
    del self.blocks[val]

  def __del__(self):
    for b in self.blocks:
      del b

  def add(self, block):
    self.blocks.append(block)
    # 新たなブロックの高さが元のチェーンの高さ超過ならばlastを更新
    if(block.height > self.last.height):
      self.last = block

  def pop(self, index):
    return self.blocks.pop(index)

  def copy(self, cpyfrom):
    self.blocks = copy.copy(cpyfrom)
    self.last = cpyfrom.last
