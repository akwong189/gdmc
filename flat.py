import numpy as np
from NBTBuildings import NBTBuildings, Cardinals

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)  # this takes a while

ROADHEIGHT = 0
heights = np.array(WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"])
x_max, z_max = heights.shape

binary_mask = np.zeros(shape=(x_max, z_max))

house = NBTBuildings("./villages/plains/houses/plains_small_house_2.nbt")
h_x, h_y, h_z = house.get_size()

for x in range(x_max):
    for z in range(z_max):
        location = heights[x : x + h_x, z : z + h_z]
        mask = binary_mask[x : x + h_x, z : z + h_z]

        # print(location.shape == (h_x, h_z), location.max() == location.min(), mask.max() == 0 and mask.min() == 0)
        if (
            location.shape == (h_x, h_z)
            and location.max() == location.min()
            and mask.max() == 0
            and mask.min() == 0
        ):
            print(f"Building house at {x},{location.min()},{z}")
            house.place_structure(
                INTF, x, location.min(), z, Cardinals.NORTH
            )
            #     x += h_x
            #     z += h_z
            binary_mask[x : x + h_x + 2, z : z + h_z + 2] = 1

# print(f"Placing cobblestone at {0}, {heights[0][0]}, {0}")
# INTF.placeBlock(0, heights[129][129], 0, "cobblestone")
