from distutils.command.build import build
from time import sleep
from NBTBuildings import NBTBuildings
from pathing import create_path
from gdpc import interface as INTF
from gdpc import worldLoader as WL
from rich.console import Console
import numpy as np
import glob
import time
import villager
import eventSystem
import events

from visualize import generate_mask, display_masked_map
from draw import draw_line, place_structure
from placeVillagers import summon_villagers, summon_husks, summon_lightning

import random

console = Console()

def get_plains_buildings(path="./villages/plains/houses"):
    """Glob the plains building nbt from path

    Args:
        path (str, optional): path to buildings. Defaults to "./villages/plains/houses".

    Returns:
        list: list of nbt paths
    """
    return glob.glob(f"{path}/*.nbt")

def get_savanna_buildings(path="./villages/savanna/houses"):
    """Glob the savanna building nbt from path

    Args:
        path (str, optional): path to buildings. Defaults to "./villages/savanna/houses".

    Returns:
        list: list of nbt paths
    """
    return glob.glob(f"{path}/*.nbt")

def get_desert_buildings(path="./villages/desert/houses"):
    """Glob the desert building nbt from path

    Args:
        path (str, optional): path to buildings. Defaults to "./villages/desert/houses".

    Returns:
        list: list of nbt paths
    """
    return glob.glob(f"{path}/*.nbt")

def get_snowy_buildings(path="./villages/snowy/houses"):
    """Glob the snowy building nbt from path

    Args:
        path (str, optional): path to buildings. Defaults to "./villages/snowy/houses".

    Returns:
        list: list of nbt paths
    """
    return glob.glob(f"{path}/*.nbt")


if __name__ == "__main__":
    with console.status(
        "[bold green]Procedural village generation in progress..."
    ) as status:
        STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

        # Generate a border around build area
        for x in range(STARTX, ENDX):
            INTF.placeBlock(x, 128, STARTZ, "cobblestone")
            INTF.placeBlock(x, 128, ENDZ, "cobblestone")

        for z in range(STARTZ, ENDZ):
            INTF.placeBlock(STARTX, 128, z, "cobblestone")
            INTF.placeBlock(ENDX, 128, z, "cobblestone")
        console.log("Created border")

        intf = INTF.Interface(STARTX, STARTY, STARTZ, caching=True)
        WORLDSLICE = WL.WorldSlice(
            STARTX, STARTZ, ENDX + 1, ENDZ + 1
        )  # this takes a while
        heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

        x_max, z_max = heights.shape
        center_x = (ENDX - STARTX) // 2
        center_z = (ENDZ - STARTZ) // 2

        # generate paths
        create_path(
            path_start_x=STARTX + center_x,
            path_start_z=STARTZ + center_z,
            path_length=10,
            path_min=5,
            path_max=10,
            heights=heights,
        )
        console.log("Created paths")

        # mask = np.zeros(shape=heights.shape)
        mask = generate_mask(STARTX, STARTZ, ENDX, ENDZ, heights)
        console.log("Created Mask")

        savanna_biomes = ["savanna", "savanna_plateau", "shattered_savanna", "shattered_savanna_plateau"]
        snowy_biomes = ["snowy_beach", "snowy_mountains", "snowy_taiga", "snowy_taiga_hills", "snowy_taiga_mountains", "snowy_tundra"]
        desert_biomes = ["desert", "desert_hills", "desert_lakes"]
        build_biome = WORLDSLICE.getBiomeAt(STARTX + center_x, heights[STARTX + center_x][STARTZ + center_z], STARTZ + center_z)

        #insert town center
        if build_biome in savanna_biomes:
            well = NBTBuildings(
                "./villages/savanna/town_centers/savanna_meeting_point_1.nbt", y_offset=1
            )
        elif build_biome in snowy_biomes:
            well = NBTBuildings(
                "./villages/snowy/town_centers/snowy_meeting_point_1.nbt", y_offset=1
            )
        elif build_biome in desert_biomes:
            well = NBTBuildings(
                "./villages/desert/town_centers/desert_meeting_point_1.nbt", y_offset=1
            )
        else:
            well = NBTBuildings(
                "./villages/plains/town_centers/plains_meeting_point_1.nbt", y_offset=1
            )

        x, _, z = well.get_size()

        sleep(1)
        place_structure(
            heightmap=heights,
            mask=mask,
            x=STARTX + center_x - x // 2,
            z=STARTZ + center_z - z // 2,
            structure=well,
            ignore_path=True,
            pad=1
        )
        sleep(1.5)
        console.log(
            f"Placing Well at {STARTX + center_x - x//2} {heights[center_x - x//2, center_z - x//2]} {STARTZ + center_z - z//2}"
        )

        # place houses
        houses = []
        if build_biome in savanna_biomes:
            for h in get_savanna_buildings():
                houses.append(NBTBuildings(h))
        elif build_biome in snowy_biomes:
             for h in get_snowy_buildings():
                houses.append(NBTBuildings(h))
        elif build_biome in desert_biomes:
            for h in get_desert_buildings():
                houses.append(NBTBuildings(h))
        else:
            for h in get_plains_buildings():
                houses.append(NBTBuildings(h))


        sleep(1)
        villager_houses = []
        for x in range(5, x_max):
            for z in range(5, z_max):
                np.random.shuffle(houses)
                for house in houses:
                    if place_structure(
                        heightmap=heights,
                        mask=mask,
                        x=STARTX + x,
                        z=STARTZ + z,
                        structure=house,
                        path_radius=3,
                        pad=1,
                    ):
                        if "_house_" in house.path:
                            villager_houses.append((STARTX + x, heights[STARTX + x][STARTZ + z], STARTZ + z))
                        break
        
        WORLDSLICE = WL.WorldSlice(
            STARTX, STARTZ, ENDX + 1, ENDZ + 1
        )  # this takes a while
        heights_houses = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
        villager_house_tops = []
        for vh in villager_houses:
            villager_house_tops.append((vh[0], heights_houses[vh[0]][vh[2]], vh[2]))

        #generate villager data
        villagers = []
        for vh in villager_house_tops:
            villagers.append(villager.Villager(vh))

        #generate relationships
        for villager in villagers:
            villager.generate_relationships(villagers)

        chanceOfAnger = random.randint(0, 10)
        for villager in villagers:
            if chanceOfAnger < 5:
                villager.update_relationship(random.choice(villagers).name, -2)

        #create event manager
        e_man = eventSystem.eventManager(villagers)
        
        #generate village name
        village_name_head = ["Ever", "Mine", "Diamond", "Rune", "Wheat", 
                             "Iron", "Azul"]
        if build_biome in savanna_biomes:
            savanna_name_head = ["Savanna", "Orange", "Savanna", "Grass"]
            village_name_head.append(savanna_name_head)
        elif build_biome in snowy_biomes:
            snowy_name_head = ["Snow", "Ice", "Frost", "Frozen", "Cold"]
            village_name_head.append(snowy_name_head)
        elif build_biome in desert_biomes:
            desert_name_head = ["Desert", "Oasis", "Cactus", "Sand", "Scorch"]
            village_name_head.append(desert_name_head)
        else:
            plains_name_head = ["Flat", "Plane", "Dirt", "Grass", "Coal"]
        village_name_tail = ["landia", "ia", "opolis", "ica", "is", "opolis", "lands"]
        village_name = random.choice(village_name_head) + random.choice(village_name_tail) + " Village"
        #populate village
        INTF.runCommand("title @a title {\"text\":\"\",\"extra\":[{\"text\":\"" + "Villagers have moved in to " + village_name + "\",\"color\":\"" + "yellow" + "\",\"bold\":\"true\"}]}")
        print(len(villagers))
        events.summon_entities(e_man, "summon_villagers", (STARTX + center_x, heights[STARTX + center_x][STARTZ + center_z], STARTZ + center_z), 7, 10, "villager", len(villagers))
        e_man.run_event()
        #first event
        time.sleep(5)
        INTF.runCommand("title @a title {\"text\":\"\",\"extra\":[{\"text\":\"" + "Lightning Strike Incoming!" + "\",\"color\":\"" + "yellow" + "\",\"bold\":\"true\"}]}")
        events.summon_entities(e_man, "summon_lightning", random.choice(villager_house_tops), 1, 10, "minecraft:lightning_bolt", 5)
        e_man.run_event()

        # display visualizations        
        img = display_masked_map(heights, mask)
        img.show()
