from PIL import Image
import numpy as np

PX_SIZE = 4

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
    color_step = 255 // (max_height - min_height)

    for _x in range(x):
        for _z in range(z):
            height = height_map[_x, _z]
            color = color_step * (height - min_height)
            draw_pixel(img, _x*PX_SIZE, _z*PX_SIZE, (_x+1)*PX_SIZE, (_z+1)*PX_SIZE, (0, color, 0))


def display_mask(mask, img=None):
    x, z = mask.shape
    if img == None:
        img = Image.new('RGB', (x*PX_SIZE, z*PX_SIZE))
    pass

def display_masked_map(heightmap, mask):
    x, z = height_map.shape
    img = Image.new('RGB', (x*PX_SIZE, z*PX_SIZE))
    pass

def generate_heightmap(min_height, max_height, size=(256, 256)):
    return np.random.uniform(low=min_height, high=max_height, size=size).astype(int)

if __name__ == "__main__":
    height_map = generate_heightmap(64, 70)
    img = display_height_map(height_map)
    img.show()