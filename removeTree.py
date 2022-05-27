from nbt import nbt
from enum import Enum

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL
STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
                           ENDX + 1, ENDZ + 1)  # this takes a while

heights = WORLDSLICE.heightmaps["MOTION_BLOCKING"]

def removeTree(start_x, end_x, start_z, end_z):
    shrubs = ['minecraft:oak_leaves', 'minecraft:oak_log',
        'minecraft:spruce_leaves', 'minecraft:spruce_log',
        'minecraft:birch_leaves', 'minecraft:birch_log',
        'minecraft:jungle_leaves', 'minecraft:jungle_log',
        'minecraft_vine']
    for x in range (start_x, end_x):
        for z in range(start_z, end_z):
            cur_height = heights[x,z] - 1
            block = INTF.getBlock(x, cur_height, z)
            # print(f'{x}, {cur_height}, {z}: {block}')

            # while the block is a leaf or tree
            # replace with air
            while block in shrubs:
                INTF.placeBlock(x, cur_height, z, "air")
                cur_height -= 1
                block = INTF.getBlock(x, cur_height, z)
                # print(f'{x}, {cur_height}, {z}: {block}')


if __name__ == '__main__':
    # NOTE: It is a good idea to keep this bit of the code as simple as
    #     possible so you can find mistakes more easily

    try:
        height = WORLDSLICE.heightmaps["MOTION_BLOCKING"][(STARTX, STARTY)]
        # INTF.runCommand(f"tp @a {STARTX} {height} {STARTZ}")
        # print(f"/tp @a {STARTX} {height} {STARTZ}")
        print('Running remove tree command')
        # removeTree(STARTX, STARTX+10, STARTZ, STARTZ+10)
        # removeTree(3, 8, 15, 20)
        # removeTree(0, 6, 12, 19)
        removeTree(STARTX, ENDX, STARTZ, ENDZ)


    except KeyboardInterrupt:   # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")