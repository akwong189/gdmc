from nbt import nbt
from enum import Enum

class Cardinals(Enum):
    NORTH=1
    EAST=2
    SOUTH=3
    WEST=4

from random import randint

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL
STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
                           ENDX + 1, ENDZ + 1)  # this takes a while

ROADHEIGHT = 0

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
    i = 0
    
    for p in nbtfile["palette"]:
        block = p["Name"].value.replace("minecraft:", "")
        
        if p.get("Properties") != None:
            properties = []
            for t in p["Properties"].tags:
                properties.append(f"{t.name}={t.value}")
            block += f"[{','.join(properties)}]"
        block_map[i] = block
        i += 1
        
    print(block_map)
    block_loc = []
    
    for b in nbtfile["blocks"]:
        pos = b['pos']
        x, y, z = pos[0].value, pos[1].value, pos[2].value
        block_id = b['state'].value
        
        if b.get("nbt") != None and b.get("nbt").get("final_state") != None:
            # print(b["nbt"])
            block = b.get("nbt")["final_state"].value.replace("minecraft:", "")
        else:
            block = block_map[block_id]
        
        if block != "air":
            block_data = {"location": (x, y, z), "block": block}
            block_loc.append(block_data)
    print(block_loc)
    return block_loc
        
        
        
if __name__ == "__main__":
    blocks = place_structure("./villages/plains/houses/plains_small_house_1.nbt", 0, 0, 0, Cardinals.NORTH)
    
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    print(STARTX, STARTY + 128, STARTZ)
    
    for d in blocks:
        x, y, z = d["location"]
        INTF.placeBlock(STARTX + x, STARTY + y + 128, STARTZ + z, d["block"])