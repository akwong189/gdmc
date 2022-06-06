from random import randint
from gdpc import interface as INTF
from gdpc import worldLoader as WL
from queue import Queue
import eventSystem
import time

def summon_entities(eventSystem, eventName, location, minDist, maxDist, entName, numEnt):
    """Summon certain entities and send information to the event system.

    Args:
        eventSystem (eventManager): system handling the events to be executed
        eventName (str): event to be executed. Ex: "summon_villagers"
        location ((int, int, int)): tuple of base x, y, and z coordinates to summon entities
        minDist (int): minimum distance away from the base location to summon entities
        maxDist (int): maximum distance away from the base location to summon entities
        entName (str): entity to be summoned. Ex: "villager"
        numEnt (int): number of entities to be summoned
    """
    #populate with n villagers
    for f in range(numEnt):
        if eventName == "summon_lightning":
            time.sleep(1)
        #randomize villagers distance from start location
        firstRand = randint(minDist, maxDist)
        secondRand = randint(minDist, maxDist)
        #randomize direction from start location
        if (randint(0,1) == 1):
            firstRand = firstRand * -1
        if (randint(0,1) == 1):
            secondRand = secondRand * -1
        #place entity
        summonX = location[0] + firstRand
        summonY = location[1]
        summonZ = location[2] + secondRand

        INTF.runCommand("summon " + entName + " {} {} {}".format(summonX, summonY, summonZ))
    eventSystem.send_to_event_system(eventName, (location[0], location[1], location[2]))