from nbt import nbt
from enum import Enum
import numpy as np

from visualize import display_masked_map

class Cardinals(Enum):
    WEST=0
    NORTH=1
    EAST=2
    SOUTH=3

VALS = {0: "west", 1: "north", 2: "east", 3: "south"}

class NBTBuildings:
    """Create a building based on NBT files
    """
    def __init__(self, nbt_path: str, y_offset=0):
        self.path = nbt_path
        self.nbt = nbt.NBTFile(nbt_path, 'rb')
        self.pallete = self._retrieve_pallete()
        self.structure_3d = np.ndarray(shape=(self.get_nbt_size()), dtype=object)
        self.y_offset = y_offset
        
        self.orientation = None

        self._retrieve_blocks()
        self.structure_3d = np.swapaxes(self.structure_3d, 0, 2)
        
    def _retrieve_pallete(self):
        """Retrieve the valid pallete from the NBT file

        Returns:
            dict: dictionary that associates index with the block and properties
        """
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
        """Retrieve the blocks in the NBT
        """
        for b in self.nbt["blocks"]:
            pos = b['pos']
            x, y, z = pos[0].value, pos[1].value, pos[2].value
            block_id = b['state'].value
            
            if b.get("nbt") != None and b.get("nbt").get("final_state") != None:
                block = b.get("nbt")["final_state"].value.replace("minecraft:", "")

                # minecraft nbt files have a predefined entrance which we can use to create an offset
                if b.get("nbt")["name"].value == "minecraft:building_entrance":
                    self.y_offset = y

                # ignore void structure blocks
                if "structure_void" in block:
                    block=""
            else:
                block = self.pallete[block_id]
            
            self.structure_3d[x, y, z] = block
            
    def _replace_facing(self, data, direction: Cardinals):
        """Replace the facing from an NBT data string with the new proper direction

        Args:
            data (str): previous facing direction of the NBT structure
            direction (Cardinals): direction which the structure will be placed

        Returns:
            str: new NBT string with proper direction
        """
        new_facing = ""
        facing = ""
        if "west" in data:
            facing = "west"
            new_facing = VALS[direction.value]
        elif "north" in data:
            facing = "north"
            new_facing = VALS[abs(direction.value + 3) % 4]
        elif "east" in data:
            facing = "east"
            new_facing = VALS[abs(direction.value + 2) % 4]
        else: # south
            facing = "south"
            new_facing = VALS[abs(direction.value + 1) % 4]
        return data.replace(facing, new_facing)
    
    def _cardinal_location(self, direction: Cardinals):
        """Rotate the structure to face the correct cardinal direction

        Args:
            direction (Cardinals): Direction that the structure should face

        Returns:
            [BuildInfo]: Resulting rotation of structure
        """
        if direction == Cardinals.EAST:
            return np.rot90(self.structure_3d, 1, axes=[0, 2])
        if direction == Cardinals.WEST:
            return np.rot90(self.structure_3d, 3, axes=[0, 2])
        if direction == Cardinals.SOUTH:
            return np.rot90(self.structure_3d, 2, axes=[0, 2])
        return self.structure_3d
    
    def get_nbt_size(self):
        """Retrieve the size of the nbt

        Returns:
            (int, int, int): size of the nbt structure
        """
        size = self.nbt["size"]
        return size[0].value, size[1].value, size[2].value

    def get_size(self):
        """Retrieve the size of the structure (includes rotation)

        Returns:
            (int, int, int): size of the 3d structure
        """
        return self.structure_3d.shape
    
    # def rotate(self, direction: Cardinals=Cardinals.WEST):
    #     structure = self._cardinal_location(direction=direction)
    #     s_x, s_y, s_z = structure.shape

    #     for _x in range(s_x):
    #         for _y in range(s_y):
    #             for _z in range(s_z):
    #                 d = structure[_x][_y][_z]
    #                 if d not in ("None", None, ""):
    #                     data = str(d)
    #                     if "facing" in data:
    #                         data = self._replace_facing(data, direction)

    def place(self, intf, x: int, y: int, z: int, direction: Cardinals=Cardinals.WEST):
        """Places the structure into the build area with provided cordinates and direction

        Args:
            intf (INTF): gdpc minecraft interface
            x (int): starting x
            y (int): starting y
            z (int): starting z
            direction (Cardinals, optional): direction the structure is placed. Defaults to Cardinals.WEST.
        """
        structure = self._cardinal_location(direction=direction)
        # it =  np.nditer(structure, flags=['multi_index', "refs_ok"])

        s_x, s_y, s_z = structure.shape

        for _x in range(s_x):
            for _y in range(s_y):
                for _z in range(s_z):
                    d = structure[_x][_y][_z]
                    if d not in ("None", None, ""):
                        data = str(d)
                        if "facing" in data:
                            data = self._replace_facing(data, direction)
                        
                        intf.placeBlock(x + _x, y + _y - self.y_offset, z + _z, data)
        
    def __str__(self):
        return self.path
        
if __name__ == "__main__":
    from gdpc import interface as INTF
    from gdpc import worldLoader as WL
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
                            ENDX + 1, ENDZ + 1)  # this takes a while

    ROADHEIGHT = 0
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    
    house = NBTBuildings("./villages/plains/houses/plains_library_1.nbt")
    house.place(INTF, STARTX + 20, STARTY + 10, STARTZ - 20, Cardinals.WEST)

    img = display_masked_map(heights, mask)
    img.show()