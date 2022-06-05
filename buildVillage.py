from NBTBuildings import NBTBuildings
from pathing import create_path
from gdpc import interface as INTF
from gdpc import worldLoader as WL
from rich.console import Console
import numpy as np

from visualize import generate_mask, display_masked_map
from draw import draw_line, place_structure

console = Console()

if __name__ == "__main__":
    # args -> xcoord of start block, ycoord of start block, iterations per path, path min, path max
    """
    -paths can be thought of as a bunch of repeating "L's"
    -iterations are the number of L's per path
    -path min and path max set the bounds for the smallest/largest longitudinal/latitudal L
    -a path of 10 iterations with a min of 1 and a max of 4 will create 10 connecting L's of
        varying size; some will be just 1 block, some a 2 block L, some a 3 block L
    -if the path goes out of play area it crashes
    """

    with console.status("[bold green]Procedural village generation in progress...") as status:
        STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

        for x in range(STARTX, ENDX):
            INTF.placeBlock(x, 128, STARTZ, "cobblestone")
            INTF.placeBlock(x, 128, ENDZ, "cobblestone")

        for z in range(STARTZ, ENDZ):
            INTF.placeBlock(STARTX, 128, z, "cobblestone")
            INTF.placeBlock(ENDX, 128, z, "cobblestone")
        console.log("Created border")

        intf = INTF.Interface(STARTX, STARTY, STARTZ, caching=True)
        WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)  # this takes a while
        heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

        x_max, z_max = heights.shape
        center_x = (ENDX - STARTX) // 2
        center_z = (ENDZ - STARTZ) // 2

        create_path(
            path_start_x=STARTX + center_x,
            path_start_z=STARTZ + center_z,
            path_length=5,
            path_min=4,
            path_max=10,
            heights=heights,
        )
        console.log("Created paths")

        mask = generate_mask(STARTX, STARTZ, ENDX, ENDZ, heights)
        console.log("Created Mask")

        well = NBTBuildings("./villages/plains/town_centers/plains_meeting_point_1.nbt", y_offset=1)
        x, _, z = well.get_size()

        place_structure(heightmap=heights, mask=mask, x=STARTX + center_x - x//2, z= STARTZ + center_z - z//2, structure=well, ignore_path=True)
        console.log(f"Placing Well at {STARTX + center_x - x//2} {heights[center_x - x//2, center_z - x//2]} {STARTZ + center_z - z//2}")

        # place house
        houses = [NBTBuildings("./villages/plains/houses/plains_small_house_1.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_2.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_3.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_4.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_5.nbt", 1),
              NBTBuildings("./villages/plains/houses/plains_small_house_6.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_7.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_8.nbt", 2),
              NBTBuildings("./villages/plains/houses/plains_medium_house_1.nbt", 1)]

        np.random.shuffle(houses)
        
        for x in range(5, x_max):
            for z in range(5, z_max):
                house = np.random.choice(houses)
                place_structure(heightmap=heights, mask=mask, x=STARTX+x, z=STARTZ+z, structure=house, path_radius=3)

        img = display_masked_map(heights, mask)
        img.show()