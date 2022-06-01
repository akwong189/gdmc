from nbt import nbt
from enum import Enum
import numpy as np

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

heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

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

def place_blocks_x(intermediate_block, start_block):
    x = 0
    z = 2
    x_delt = intermediate_block[x] - start_block[x]
    x_mag = abs(x_delt)

    #place blocks in x direction
    for i in range(x_mag - 1):
        y_placement = heights[start_block[x] + (1 * (int)(x_delt / x_mag)) + (i * (int)(x_delt / x_mag))][start_block[z]] - 1
        if INTF.getBlock(start_block[x] + (1 * (int)(x_delt / x_mag)) + (i * (int)(x_delt / x_mag)), y_placement, start_block[z]) == "minecraft:water":
            INTF.placeBlock(start_block[x] + (1 * (int)(x_delt / x_mag)) + (i * (int)(x_delt / x_mag)), y_placement, start_block[z], "oak_planks")
        else:
            INTF.placeBlock(start_block[x] + (1 * (int)(x_delt / x_mag)) + (i * (int)(x_delt / x_mag)), y_placement, start_block[z], "grass_path")

def place_blocks_z(intermediate_block, end_block):
    x = 0
    z = 2
    z_delt = end_block[z] - intermediate_block[z]
    z_mag = abs(z_delt)
    
    #place blocks in z direction
    for j in range(z_mag - 1):
        y_placement = heights[intermediate_block[x]][(intermediate_block[z] + (1 * (int)(z_delt / z_mag))) + (j * (int)(z_delt / z_mag))] - 1
        if INTF.getBlock(intermediate_block[x], y_placement, (intermediate_block[z] + (1 * (int)(z_delt / z_mag))) + (j * (int)(z_delt / z_mag))) == "minecraft:water":
            INTF.placeBlock(intermediate_block[x], y_placement, (intermediate_block[z] + (1 * (int)(z_delt / z_mag))) + (j * (int)(z_delt / z_mag)), "oak_planks")
        else:
            INTF.placeBlock(intermediate_block[x], y_placement, (intermediate_block[z] + (1 * (int)(z_delt / z_mag))) + (j * (int)(z_delt / z_mag)), "grass_path")
        
if __name__ == "__main__":
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    start_block = (68, heights[68][30], 30)
    blocks = place_structure("./well.nbt", 0, 0, 0, Cardinals.NORTH)
    
    print(STARTX, STARTY + 128, STARTZ)

    for d in blocks:
        x, y, z = d["location"]
        INTF.placeBlock(STARTX + x + start_block[0], STARTY + y + heights[start_block[0]][start_block[2]] - 9, STARTZ + z + start_block[2], d["block"])

    x = 0
    y = 1
    z = 2

    mask = np.zeros(shape=heights.shape)
    start_block = (STARTX, heights[STARTX, STARTZ], STARTZ)

    #initialize modifier    
    x_modifier = 1
    z_modifier = 1
    #run in all 4 directions
    for l in range(4):
        #l==0 is positive x direction
        #negative z direction
        if l == 1:
            x_modifier = -1
        #negative x direction
        if l == 2:
            x_modifier = -1
        #positive z direction
        if l == 3:
            x_modifier = 1
        #run pathing 5 times branching outwards
        for i in range(5):
            #path lengths between 4 and 10 blocks
            x_distance = randint(4, 10)
            z_divergence_diff = randint(-x_distance, x_distance)
            #set end block based on random values
            end_block_x = (start_block[x] + (x_distance * x_modifier))
            end_block_z = start_block[z] + z_divergence_diff
            #if l is odd then start in z direction
            if l == 1 or l == 3:
                end_block_x = start_block[x] + z_divergence_diff
                end_block_z = (start_block[z] + (x_distance * x_modifier))
            
            #check to see if pathing end blocks will be too high up/down low
            breakCheck = False
            for j in range(100):
                if (abs((heights[end_block_x][end_block_z]) - (heights[end_block_x][start_block[z]])) > 2 or abs((heights[end_block_x][start_block[z]]) - start_block[y]) > 2):
                    x_distance = randint(4, 10)
                    z_divergence_diff = randint(-x_distance, x_distance)
                    end_block_x = (start_block[x] + (x_distance * x_modifier))
                    end_block_z = (start_block[z] + start_block[z] + z_divergence_diff)
                    if l == 1 or l == 3:
                        end_block_x = start_block[x] + z_divergence_diff
                        end_block_z = (start_block[z] + (x_distance * x_modifier))
                    if j == 99:
                        breakCheck = True
            
            #no suitable pathing available
            if breakCheck == True:
                break
            
            #set end block and intermediate block to go on height maps
            end_block = (end_block_x, heights[end_block_x][end_block_z], end_block_z)
            intermediate_block = (end_block[x], heights[end_block[x]][start_block[z]], start_block[z])

            #place down the starting, ending, and intermediate blocks
            INTF.placeBlock(start_block[x], heights[start_block[x]][start_block[z]] - 1, start_block[z], "grass_path")
            INTF.placeBlock(end_block[x], heights[end_block[x]][end_block[z]] - 1, end_block[z], "grass_path")
            INTF.placeBlock(intermediate_block[x], heights[intermediate_block[x]][intermediate_block[z]] - 1, intermediate_block[z], "grass_path")

            #placex
            place_blocks_x(start_block, intermediate_block)

            #placez
            place_blocks_z(intermediate_block, end_block)

            second_start = (start_block[x] + 1, heights[start_block[x]][start_block[z] + 1], start_block[z] + 1)
            second_end = (end_block[x] + 1, heights[end_block[x]][end_block[z] + 1], end_block[z] + 1)
            second_intermediate = (second_end[x], heights[second_end[x]][second_start[z]], second_start[z])
            
            #place down the starting, ending, and intermediate blocks
            INTF.placeBlock(second_start[x], second_start[y] - 1, second_start[z], "grass_path")
            INTF.placeBlock(second_end[x], second_end[y] - 1, second_end[z], "grass_path")
            INTF.placeBlock(second_intermediate[x], second_intermediate[y] - 1, second_intermediate[z], "grass_path")
            place_blocks_x(second_start, second_intermediate)

            place_blocks_z(second_intermediate, second_end)

            #temp
            INTF.placeBlock(start_block[x], heights[start_block[x]][start_block[z]] - 1, start_block[z], "grass_path")
            INTF.placeBlock(end_block[x], heights[end_block[x]][end_block[z]] - 1, end_block[z], "grass_path")
            INTF.placeBlock(intermediate_block[x], heights[intermediate_block[x]][intermediate_block[z]] - 1, intermediate_block[z], "grass_path")

            print(heights)
            #reset start block in the same cardinal direction
            start_block = end_block
        
        #reset start block for new cardinal direction
        start_block = (68, heights[68][30], 30)
