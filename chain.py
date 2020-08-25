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

  def add(self, block):
    self.blocks.append(block)
    if(block.height > self.last.height):
      self.last = block
