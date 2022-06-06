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

if __name__ == "__main__":

    villagers = []
    locations = [(4, 4, 4), (0, 4, 4), (1, 4, 4), (2, 4, 4), (3, 4, 4), (4, 3, 4), (0, 2, 4), (1, 5, 4), (2, 6, 4), (3, 8, 4)]
    for vh in locations:
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

    print("------------------test begin-------------------")
    INTF.runCommand("title @a title {\"text\":\"\",\"extra\":[{\"text\":\"" + "Lightning Strike Incoming!" + "\",\"color\":\"" + "yellow" + "\",\"bold\":\"true\"}]}")
    events.summon_entities(e_man, "summon_lightning", random.choice(locations), 1, 10, "minecraft:lightning_bolt", 5)
    e_man.run_event()
    print("------------------test end---------------------")
    