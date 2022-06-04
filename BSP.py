# from nbt import nbt
# from enum import Enum
import numpy as np

# from gdpc import geometry as GEO
# from gdpc import interface as INTF
# from gdpc import toolbox as TB
# from gdpc import worldLoader as WL
# STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

# WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
#                            ENDX + 1, ENDZ + 1)  # this takes a while

# heights = WORLDSLICE.heightmaps["MOTION_BLOCKING"]

def drawBoundaries():
    # drawing the boundaries of the build area for visualization purposes
    for z in range(STARTZ, ENDZ + 1):
        INTF.placeBlock(STARTX, 100, z, "redstone_block")
        INTF.placeBlock(ENDX, 100, z, "redstone_block")

    for x in range(STARTX, ENDX + 1):
        INTF.placeBlock(x, 100, STARTZ, "redstone_block")
        INTF.placeBlock(x, 100, ENDZ, "redstone_block")

def drawXAxis():
    # drawing x axis
    xaxis = STARTX + (ENDX - STARTX) // 2  # getting start + half the length

    for z in range(STARTZ, ENDZ + 1):
        INTF.placeBlock(xaxis, 100, z, "redstone_block")

def drawZAxis():
    zaxis = STARTZ + (ENDZ - STARTZ) // 2
    # drawing z axis
    for x in range(STARTX, ENDX + 1):
        INTF.placeBlock(x, 100, zaxis, "redstone_block")

# need to create a function to split a chunk, given startx endx startz endz

def generate_district_mask(x1, z1, x2, z2, arr):
    mask = np.zeros(shape=height.shape)
    
    for x in range(x2 - x1):
        for z in range(z2 - z1):
            continue
            # block = INTF.getBlock(x, height[x,z]-1, z)
            # if block == "minecraft:water":
            #     mask[x1+x,z1+z] = 2
            # elif block == "minecraft:lava":
            #     mask[x1+x,z1+z] = 4
            # elif block == "minecraft:grass_paths":
            #     mask[x1+x,z1+z] = 3
            # elif block == "minecraft:oak_planks":
            #     mask[x1+x,z1+z] = 3
    return mask


def binarySpacePartition():
    # arr = np.zeros(shape=heights.shape)
    arr = np.zeros((128,128))
    
    minX = 10
    minZ = 10
    axis = 0

    count = 0
    id = 0

    print(arr)
    indices = numpy.transpose(numpy.nonzero(arr == count))
    

    print(indices)

    # how to mark a partition? how should it be represented
    # randomly select a partition, check if it meets min sizes
    # if so, split it in two

    # while count < some value
    
        # get random partition
        # check area > minX, minZ
        # if yes, split partition in half, along x or z axis
        # if no, select other chunk
    
    return

if __name__ == '__main__':
    # NOTE: It is a good idea to keep this bit of the code as simple as
    #     possible so you can find mistakes more easily

    try:
        # height = WORLDSLICE.heightmaps["MOTION_BLOCKING"][(STARTX, STARTY)]
        # INTF.runCommand(f"tp @a {STARTX} {height} {STARTZ}")
        # print(f"/tp @a {STARTX} {height} {STARTZ}")

        # drawBoundaries()
        # drawXAxis()
        binarySpacePartition()

    except KeyboardInterrupt:   # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")