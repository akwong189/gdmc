from nbt import nbt
from enum import Enum

class Cardinals(Enum):
    NORTH=1
    EAST=2
    SOUTH=3
    WEST=4

class Block:
    def __init__(self, x, y, z, block=None, direction=Cardinals.NORTH):
        self.block = block
        self.x = x
        self.y = y
        self.z = z
        self.direction = direction

    def set_block(self, block: str):
        self.block = block
        
    def set_location(self, x: int =None, y: int =None, z: int =None, direction: Cardinals =None):
        if x: self.x = x
        if y: self.y = y
        if z: self.z = z
        if direction: self.direction = direction
        
    def get_block(self):
        return
        
def place_block(intf, start_x, start_y, start_z, block: Block):
    intf.placeBlock(start_x + block.x, start_y + block.y, start_z + block.z, start_x + block.x + 1, start_y + block.y + 1, start_z + block.z + 1, block.block)

def place_structure(nbt_path: str, x: int, y: int, z: int, direction: Cardinals):
    nbtfile = nbt.NBTFile(nbt_path, 'rb')
    
    block_map = {}
    
    for b in nbtfile["blocks"]:
        pos = b['pos']
        x, y, z = pos[0].value, pos[1].value, pos[2].value
        block_id = b['state'].value
        
        
        
if __name__ == "__main__":
    place_structure("./villages/plains/houses/plains_small_house_1.nbt", 0, 0, 0, Cardinals.NORTH)