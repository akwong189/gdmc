from PIL import Image
import numpy as np
from gdpc import interface as INTF

PX_SIZE = 4

COLOR_VALUES = {
    1: (235, 235, 83), # building
    2: (108, 207, 255), # water
    3: (114, 64, 31), # path
    4: (247, 112, 22), # lava
    5: (100, 0, 0), # do not build zone
    6: (47, 249, 148), # do not build zone for lamps/roads
}

def draw_pixel(img, x1, z1, x2, z2, color):
    for x in range(x1, x2):
        for z in range(z1, z2):
            img.putpixel((x, z), color)

def display_height_map(height_map, img=None):
    x, z = height_map.shape
    if img == None:
        img = Image.new('RGB', (x*PX_SIZE, z*PX_SIZE))
    
    min_height = height_map.min()
    max_height = height_map.max()
    color_step = 100 // (max_height - min_height)

    for _x in range(x):
        for _z in range(z):
            height = height_map[_x, _z]
            color = 100 + color_step * (height - min_height)
            draw_pixel(img, _x*PX_SIZE, _z*PX_SIZE, (_x+1)*PX_SIZE, (_z+1)*PX_SIZE, (0, color, 0))
    return img


def display_mask(mask, img=None):
    x, z = mask.shape
    if img == None:
        img = Image.new('RGB', (x*PX_SIZE, z*PX_SIZE))
    
    for _x in range(x):
        for _z in range(z):
            color = COLOR_VALUES.get(mask[_x, _z])
            if color:
                draw_pixel(img, _x*PX_SIZE, _z*PX_SIZE, (_x+1)*PX_SIZE, (_z+1)*PX_SIZE, color)
    return img

def display_masked_map(heightmap, mask):
    img = display_height_map(height_map=heightmap)
    img = display_mask(mask, img=img)
    return img

def generate_heightmap(min_height, max_height, size=(256, 256)):
    return np.random.uniform(low=min_height, high=max_height, size=size).astype(int)

def generate_mask(x1, z1, x2, z2, height):
    mask = np.zeros(shape=height.shape)
    
    for x in range(x2 - x1):
        for z in range(z2 - z1):
            block = INTF.getBlock(x, height[x,z]-1, z)
            if block == "minecraft:water":
                mask[x1+x,z1+z] = 2
            elif block == "minecraft:lava":
                mask[x1+x,z1+z] = 4
            elif block == "minecraft:grass_paths":
                mask[x1+x,z1+z] = 3
            elif block == "minecraft:oak_planks":
                mask[x1+x,z1+z] = 3
    return mask

if __name__ == "__main__":
    from gdpc import toolbox as TB
    from gdpc import worldLoader as WL
    
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)  # this takes a while

    ROADHEIGHT = 0
    heights = np.array(WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"])
    
    # mask = np.load("mask.npy")
    mask = generate_mask(STARTX, STARTZ, ENDX+1, ENDZ+1, heights) # this takes a long time
    img = display_masked_map(heights, mask)
    img.show()
    np.save("mask", mask)