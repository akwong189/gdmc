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
        INTF.runCommand("summon villager {} {} {}".format(x_loc + firstRand, heights[x_loc + firstRand][z_loc + secondRand], z_loc + secondRand))
    '''INTF.runCommand("summon husk 79 5 71")
    INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"Hi There!\",\"color\":\"aqua\",\"bold\":\"true\"}]}")
    INTF.runCommand("summon minecraft:lightning_bolt 79 5 71")'''
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
    summon_villagers(70, 70)