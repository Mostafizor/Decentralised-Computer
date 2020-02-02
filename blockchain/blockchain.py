class Blockchain(object):
    def __init__(self):
        self.chain = []
    
    def addBlock(self, block):
        self.chain.append(block)