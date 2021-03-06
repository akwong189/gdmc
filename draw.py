from math import sqrt
import numpy as np
from NBTBuildings import Cardinals, NBTBuildings
from visualize import display_masked_map, generate_mask
from gdpc import interface as INTF

# determine the closest path to the center of the structure
def closest_path(center, paths):
    """determine the closest path from the center

    Args:
        center ((int, int)): Center location for the structure
        paths ([(int, int)]): List of path block in (x, z)

    Returns:
        Cardinal: Cardinal direction that the structure should face
    """
    closest = None
    loc = None
    
    for p in paths:
        distance = sqrt(np.square(p[0] - center[0]) + np.square(p[1] - center[1]))
        if closest is None or distance < closest:
            closest = distance
            loc = p
    return to_cardinal(loc, center)

def to_cardinal(points, center):    
    """Convert points to cardinal direction

    Args:
        points ((int, int)): Point where the path is location
        center ((int, int)): Center point

    Returns:
        Cardinal: Cardinal direction that the point is facing
    """
    deg = np.rad2deg(np.arctan2(points[1] - center[1], points[0] - center[0]))
    
    if -45 <= deg <= 45:
        return Cardinals.EAST
    elif 45 < deg <= 135:
        return Cardinals.SOUTH
    elif -135 <= deg < -45:
        return Cardinals.NORTH
    else:
        return Cardinals.WEST
        

def draw_line(intf, start_x, start_z, end_x, end_z, heightmap, mask):
    """Draw a straight line

    Args:
        intf (INTF): GDPC minecraft interface
        start_x (int): Starting X location
        start_z (int): Starting Z location
        end_x (int): Ending X location
        end_z (int): Ending Z location
        heightmap ([int]): numpy array of heights
        mask ([int]): numpy array for mask

    Returns:
        mask: numpy array for mask with straight roads
    """
    x_path = 64
    
    for i in range(128):
        intf.placeBlock(start_x + x_path, heightmap[x_path, i] - 1, start_z + i, "gravel")
        intf.placeBlock(start_x + x_path + 1, heightmap[x_path, i] - 1, start_z + i, "gravel")
        intf.placeBlock(start_x + x_path - 1, heightmap[x_path, i] - 1, start_z + i, "gravel")
        
        intf.placeBlock(start_z + i, heightmap[x_path, i] - 1, start_x + x_path, "gravel")
        intf.placeBlock(start_z + i, heightmap[x_path, i] - 1, start_x + x_path + 1, "gravel")
        intf.placeBlock(start_z + i, heightmap[x_path, i] - 1, start_x + x_path - 1, "gravel")
        
        mask[x_path-2:x_path+2, i] = 6
        mask[i, x_path-2:x_path+2] = 6
        
        mask[x_path-1:x_path+1, i] = 3
        mask[i, x_path-1:x_path+1] = 3
        
    return mask
        
def place_structure(heightmap, mask, x, z, structure, pad=2, path_radius=4, ignore_path=False):
    """Given a structure and location, determine if it can be placed at that location

    Args:
        heightmap ([int]): Height map numpy array
        mask ([int]): Mask for generation
        x (int): starting X location
        z (int): starting Z location
        structure (NBTBuilding): nbt building class
        pad (int, optional): Building padding to deter too close generation. Defaults to 2.
        path_radius (int, optional): radius to find if a path exists. Defaults to 4.
        ignore_path (bool, optional): ignore the path requirement. Defaults to False.

    Returns:
        bool: if a building can be generated (True) else (False)
    """
    h_x, h_y, h_z = structure.get_size()
    location = heightmap[x : x + h_x, z : z + h_z]
    check_mask  = mask[max(x - pad, 0) : x + h_x + pad, max(z - pad, 0) : z + h_z + pad]
    path_mask = mask[x - path_radius : x + h_x + path_radius, z - path_radius : z + h_z + path_radius]
    
    if ignore_path:
        structure.place(
            INTF, x, location.min(), z
        )
        mask[x - pad : x + h_x + pad, z - pad : z + h_z + pad] = 5
        mask[x : x + h_x , z : z + h_z] = 1
        return True

    has_path = (path_mask == 3).nonzero()
    if len(has_path[0]) == len(has_path[1]) == 0:
        return False
        
    paths = np.column_stack(has_path)

    if (
        location.shape == (h_x, h_z)
        and location.max() == location.min()
        and check_mask.max() == 0
        and check_mask.min() == 0
    ):
        middle_x, middle_z = path_mask.shape
        middle_x = middle_x // 2    
        middle_z = middle_z // 2
        
        cardinal = closest_path([middle_x, middle_z], paths)

        if cardinal not in (Cardinals.NORTH, Cardinals.SOUTH) and h_x != h_z:
            return False
        
        print(f"Placing {structure}")
        structure.place(
            INTF, x, location.min(), z, cardinal
        )
        
        mask[x - pad : x + h_x + pad, z - pad : z + h_z + pad] = 5
        mask[x : x + h_x , z : z + h_z] = 1
        return True
    return False
        
if __name__ == "__main__":
    from gdpc import worldLoader as WL
    
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
                            ENDX + 1, ENDZ + 1)  # this takes a while

    ROADHEIGHT = 0
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    x_max, z_max = heights.shape
    
    # NBTBuildings("./villages/plains/houses/plains_medium_house_2.nbt")
    houses = [NBTBuildings("./villages/plains/houses/plains_small_house_1.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_2.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_3.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_4.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_5.nbt", 1),
              NBTBuildings("./villages/plains/houses/plains_small_house_6.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_7.nbt"),
              NBTBuildings("./villages/plains/houses/plains_small_house_8.nbt", 2),
              NBTBuildings("./villages/plains/houses/plains_medium_house_1.nbt", 1),
              NBTBuildings("./villages/plains/houses/plains_library_2.nbt")]
    np.random.shuffle(houses)
    # print(houses)
    
    mask = np.zeros(shape=heights.shape)
    # mask = generate_mask(STARTX, STARTZ, ENDX+1, ENDZ+1, heights)
    mask = draw_line(INTF, STARTX, STARTZ, ENDX, ENDZ, heights, mask)  
    done = False  
    
    for x in range(5, x_max):
        for z in range(5, z_max):
            if place_structure(heightmap=heights, mask=mask, x=STARTX+x, z=STARTZ+z, structure=NBTBuildings("./villages/plains/houses/plains_library_1.nbt")):
                done = True
                break
        if done:
            break
    
    img = display_masked_map(heights, mask)
    img.show()