from random import randint
from gdpc import interface as INTF
from gdpc import worldLoader as WL
import time

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)  # this takes a while
heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

def summon_villagers(x_loc, z_loc):
    for f in range(5):
        firstRand = randint(-4, 4)
        secondRand = randint(-4, 4)
        INTF.runCommand("summon villager {} {} {}".format(x_loc + firstRand + f, heights[x_loc + firstRand + f][z_loc + secondRand + f], z_loc + secondRand + f))

    INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Craig the Villager: What a day to be alive...\",\"color\":\"aqua\",\"bold\":\"true\"}]}")
    time.sleep(5)
    INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Sarah the Villager: I was thinking the same thing, Craig!\",\"color\":\"yellow\",\"bold\":\"true\"}]}")
    '''INTF.runCommand("summon husk 79 5 71")
    INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Hi There!\",\"color\":\"aqua\",\"bold\":\"true\"}]}")
    INTF.runCommand("summon minecraft:lightning_bolt 79 5 71")'''

def summon_husks(x_loc, z_loc):
    for f in range(5):
        firstRand = randint(-10, 10)
        secondRand = randint(-10, 10)
        INTF.runCommand("summon husk {} {} {}".format(x_loc + firstRand + f, heights[x_loc + firstRand + f][z_loc + secondRand + f], z_loc + secondRand + f))
    
    INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Sarah the Villager: Are those... husks!??!\",\"color\":\"yellow\",\"bold\":\"true\"}]}")
    time.sleep(2)
    INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Jenny the Villager: RUN AWAY!!\",\"color\":\"green\",\"bold\":\"true\"}]}")
    time.sleep(2)
    INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"John the Villager: I'm too young to die!!\",\"color\":\"red\",\"bold\":\"true\"}]}")

def summon_lightning(x_loc, z_loc):
    for f in range(10):
        firstRand = randint(-10, 10)
        secondRand = randint(-10, 10)
        INTF.runCommand("summon minecraft:lightning_bolt {} {} {}".format(x_loc + firstRand + f, heights[x_loc + firstRand + f][z_loc + secondRand + f], z_loc + secondRand + f))
        time.sleep(1)
        if f == 1:
            INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Rebecca the Villager: Oh no, that's lightning!\",\"color\":\"blue\",\"bold\":\"true\"}]}")
        elif f == 3:
            INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Craig the Villager: I hope my house doesn't catch on fire!\",\"color\":\"aqua\",\"bold\":\"true\"}]}")

def event():
    #init game time
    gametime = INTF.runCommand("time query gametime")
    #init day time
    daytime = INTF.runCommand("time query daytime")
    flag1 = False
    flag2 = False
    flag3 = False
    start_time = time.time()
    interval = 2
    for i in range(100):
        # time.sleep(start_time + i*interval - time.time())
        currentTime = INTF.runCommand("time query gametime")
        try:
            if int(currentTime) - 200 > int(gametime) and not flag1:
                INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Craig the Villager: I smell something strange in the air...\",\"color\":\"aqua\",\"bold\":\"true\"}]}")
                flag1 = True
            if int(currentTime) - 300 > int(gametime) and not flag2:
                INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Jenny the Villager: You're just being superstitious Craig...\",\"color\":\"green\",\"bold\":\"true\"}]}")
                flag2 = True
            if int(currentTime) - 400 > int(gametime) and not flag3:
                INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Craig the Villager: SHUT UP JENNY\",\"color\":\"red\",\"bold\":\"true\"}]}")
                break
        except:
            print("fail!")

if __name__ == "__main__":
    print(WORLDSLICE.getBiomeAt(70, 70, 70))
    summon_villagers(70, 70)
    time.sleep(5)
    summon_husks(70, 70)
    time.sleep(5)
    summon_lightning(70, 70)