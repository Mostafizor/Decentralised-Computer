class Block(object):
    def __init__(self, blockHeader):
        self.blockHeader = blockHeader

    @staticmethod
    def genesis(GENESIS_DATA):
        return Block(GENESIS_DATA)

    