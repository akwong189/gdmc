from nbt import nbt
from enum import Enum



from random import randint

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL
STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
                           ENDX + 1, ENDZ + 1)  # this takes a while

ROADHEIGHT = 0

class NBTBuildings:
    def __init__(self, nbt_path: str):
        self.nbt = nbt.NBTFile(nbt_path, 'rb')
        self.pallete = self._retrieve_pallete()
        self.blocks = self._retrieve_blocks()
        self.size = self._get_size()
        
    class Cardinals(Enum):
        NORTH=1
        EAST=2
        SOUTH=3
        WEST=4
        
    def _retrieve_pallete(self):
        block_map = {}
        i = 0
        
        for p in self.nbt["palette"]:
            block = p["Name"].value.replace("minecraft:", "")
            
            if p.get("Properties") != None:
                properties = []
                for t in p["Properties"].tags:
                    properties.append(f"{t.name}={t.value}")
                block += f"[{','.join(properties)}]"
            block_map[i] = block
            i += 1
        return block_map
        
    def _retrieve_blocks(self):    
        block_loc = []
        
        for b in self.nbt["blocks"]:
            pos = b['pos']
            x, y, z = pos[0].value, pos[1].value, pos[2].value
            block_id = b['state'].value
            
            if b.get("nbt") != None and b.get("nbt").get("final_state") != None:
                block = b.get("nbt")["final_state"].value.replace("minecraft:", "")
            else:
                block = self.pallete[block_id]
            
            if block != "air":
                block_data = {"location": (x, y, z), "block": block}
                block_loc.append(block_data)
        return block_loc
    
    def _cardinal_location(self, location, direction):
        size = self.get_size()
    
    def get_size(self):
        size = self.nbt["size"]
        return size[0].value, size[1].value, size[2].value
    
    def place_structure(self, intf: INTF, x: int, y: int, z: int, direction: Cardinals):
        for d in self.blocks:
            _x, _y, _z = d["location"]
            intf.placeBlock(x + _x, y + _y + 128, z + _z, d["block"])
        
        
if __name__ == "__main__":
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    
    house = NBTBuildings("./villages/plains/houses/plains_small_house_2.nbt")
    house.place_structure(INTF, STARTX, STARTY, STARTZ, NBTBuildings.Cardinals.NORTH)