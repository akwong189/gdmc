from nbt import nbt
from enum import Enum
import numpy as np

class Cardinals(Enum):
    WEST=0
    NORTH=1
    EAST=2
    SOUTH=3

VALS = {0: "west", 1: "north", 2: "east", 3: "south"}

class NBTBuildings:
    def __init__(self, nbt_path: str):
        self.nbt = nbt.NBTFile(nbt_path, 'rb')
        self.pallete = self._retrieve_pallete()
        self.structure_3d = np.ndarray(shape=(self.get_size()), dtype=object)
        self.x, self.y, self.z = self.get_size()
        
        self._retrieve_blocks()
        
        
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
        for b in self.nbt["blocks"]:
            pos = b['pos']
            x, y, z = pos[0].value, pos[1].value, pos[2].value
            block_id = b['state'].value
            
            if b.get("nbt") != None and b.get("nbt").get("final_state") != None:
                block = b.get("nbt")["final_state"].value.replace("minecraft:", "")
            else:
                block = self.pallete[block_id]
            
            self.structure_3d[x, y, z] = block
            
    def _replace_facing(self, data, direction: Cardinals):
        new_facing = ""
        facing = ""
        if "west" in data:
            facing = "west"
            new_facing = VALS[direction.value]
        elif "north" in data:
            facing = "north"
            new_facing = VALS[(direction.value + 1) % 4]
        elif "east" in data:
            facing = "east"
            new_facing = VALS[(direction.value + 2) % 4]
        else: # south
            facing = "south"
            new_facing = VALS[(direction.value + 3) % 4]
        return data.replace(facing, new_facing)
    
    def _cardinal_location(self, direction: Cardinals):
        if direction == Cardinals.NORTH:
            return np.rot90(self.structure_3d, 1, axes=[0, 2])
        if direction == Cardinals.SOUTH:
            return np.rot90(self.structure_3d, 3, axes=[0, 2])
        if direction == Cardinals.EAST:
            return np.rot90(self.structure_3d, 2, axes=[0, 2])
        return self.structure_3d
    
    def get_size(self):
        size = self.nbt["size"]
        return size[0].value, size[1].value, size[2].value
    
    def place_structure(self, intf, x: int, y: int, z: int, direction: Cardinals=Cardinals.WEST):
        structure = self._cardinal_location(direction=direction)
        it =  np.nditer(structure, flags=['multi_index', "refs_ok"])
        for d in it:
            _x, _y, _z = it.multi_index
            data = str(d)
            if "facing" in data:
                data = self._replace_facing(data, direction)
            
            intf.placeBlock(x + _x, y + _y, z + _z, data)
        
        
if __name__ == "__main__":
    from gdpc import interface as INTF
    from gdpc import worldLoader as WL
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
                            ENDX + 1, ENDZ + 1)  # this takes a while

    ROADHEIGHT = 0
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    
    house = NBTBuildings("./villages/plains/houses/plains_small_house_2.nbt")
    house.place_structure(INTF, STARTX, STARTY, STARTZ, Cardinals.NORTH)