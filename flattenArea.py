from nbt import nbt
from enum import Enum

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

import numpy as np
from removeTree import removeTree

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
                           ENDX + 1, ENDZ + 1)  # this takes a while

heights = WORLDSLICE.heightmaps["MOTION_BLOCKING"]

def flattenArea(start_x, end_x, start_z, end_z):
    h = heights[start_x:end_x, start_z:end_z]
    avg_h = np.rint(h.mean())

    for x in range (start_x, end_x):
        for z in range(start_z, end_z):
            cur_height = heights[x,z]
            # print(avg_h, cur_height)
            if cur_height - avg_h == 1: # block is 1 higher
                INTF.placeBlock(x, cur_height-1, z, "air")
                heights[x,z] -= 1
            if cur_height - avg_h == -1: # block is 1 lower
                INTF.placeBlock(x, cur_height, z, "dirt")
                heights[x,z] += 1


if __name__ == '__main__':
    # NOTE: It is a good idea to keep this bit of the code as simple as
    #     possible so you can find mistakes more easily

    try:
        height = WORLDSLICE.heightmaps["MOTION_BLOCKING"][(STARTX, STARTY)]
        # print(type(height))
        INTF.runCommand(f"tp @a {STARTX} {height} {STARTZ}")
        print(f"/tp @a {STARTX} {height} {STARTZ}")
        print('Running flatten area command')
        removeTree(STARTX, STARTX+10, STARTZ, STARTZ+10)
        flattenArea(STARTX, STARTX+10, STARTZ, STARTZ+10)


    except KeyboardInterrupt:   # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")