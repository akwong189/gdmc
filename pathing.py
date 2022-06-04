from nbt import nbt
from enum import Enum
import numpy as np

from random import randint

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
                           ENDX + 1, ENDZ + 1)  # this takes a while

heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

ROADHEIGHT = 0

x = 0
y = 1
z = 2

def place_blocks_x(intermediate_block, start_block):
    x_delt = intermediate_block[x] - start_block[x]
    x_mag = abs(x_delt)

    #place blocks in x direction
    for i in range(x_mag - 1):
        y_placement = heights[start_block[x] + (1 * (int)(x_delt / x_mag)) + (i * (int)(x_delt / x_mag))][start_block[z]] - 1
        if INTF.getBlock(start_block[x] + (1 * (int)(x_delt / x_mag)) + (i * (int)(x_delt / x_mag)), y_placement, start_block[z]) == "minecraft:water" or INTF.getBlock(start_block[x] + (1 * (int)(x_delt / x_mag)) + (i * (int)(x_delt / x_mag)), y_placement, start_block[z]) == "minecraft:oak_planks":
            INTF.placeBlock(start_block[x] + (1 * (int)(x_delt / x_mag)) + (i * (int)(x_delt / x_mag)), y_placement, start_block[z], "oak_planks")
        else:
            INTF.placeBlock(start_block[x] + (1 * (int)(x_delt / x_mag)) + (i * (int)(x_delt / x_mag)), y_placement, start_block[z], "grass_path")

def place_blocks_z(intermediate_block, end_block):
    z_delt = end_block[z] - intermediate_block[z]
    z_mag = abs(z_delt)
    
    #place blocks in z direction
    for j in range(z_mag - 1):
        y_placement = heights[intermediate_block[x]][(intermediate_block[z] + (1 * (int)(z_delt / z_mag))) + (j * (int)(z_delt / z_mag))] - 1
        if INTF.getBlock(intermediate_block[x], y_placement, (intermediate_block[z] + (1 * (int)(z_delt / z_mag))) + (j * (int)(z_delt / z_mag))) == "minecraft:water" or INTF.getBlock(intermediate_block[x], y_placement, (intermediate_block[z] + (1 * (int)(z_delt / z_mag))) + (j * (int)(z_delt / z_mag))) == "minecraft:oak_planks":
            INTF.placeBlock(intermediate_block[x], y_placement, (intermediate_block[z] + (1 * (int)(z_delt / z_mag))) + (j * (int)(z_delt / z_mag)), "oak_planks")
        else:
            INTF.placeBlock(intermediate_block[x], y_placement, (intermediate_block[z] + (1 * (int)(z_delt / z_mag))) + (j * (int)(z_delt / z_mag)), "grass_path")
        
def place_corner(corner_block):
    block_type = "grass_path" #default path type

    #check for water or oak
    if INTF.getBlock(corner_block[x], heights[corner_block[x]][corner_block[z]] - 1, corner_block[z]) == "minecraft:water" or INTF.getBlock(corner_block[x], heights[corner_block[x]][corner_block[z]] - 1, corner_block[z]) == "minecraft:oak_planks":
        block_type = "oak_planks"

    INTF.placeBlock(corner_block[x], heights[corner_block[x]][corner_block[z]] - 1, corner_block[z], block_type)
    
def create_path(path_start_x, path_start_z, path_length, path_min, path_max):
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    start_block = (path_start_x, heights[path_start_x][path_start_z], path_start_z)

    #initialize modifier    
    x_modifier = 1
    #run in all 4 directions
    for l in range(4):
        #l==0 is positive x direction
        #negative z direction
        if l == 1:
            x_modifier = -1
        #negative x direction
        if l == 2:
            x_modifier = -1
        #positive z direction
        if l == 3:
            x_modifier = 1
        #run pathing 5 times branching outwards
        for i in range(path_length):
            #path lengths between 4 and 10 blocks
            x_distance = randint(path_min, path_max)
            z_divergence_diff = randint(-x_distance, x_distance)
            #set end block based on random values
            end_block_x = (start_block[x] + (x_distance * x_modifier))
            end_block_z = start_block[z] + z_divergence_diff
            #if l is odd then start in z direction
            if l == 1 or l == 3:
                end_block_x = start_block[x] + z_divergence_diff
                end_block_z = (start_block[z] + (x_distance * x_modifier))
            
            #check to see if pathing end blocks will be too high up/down low
            breakCheck = False
            for j in range(100):
                if (abs((heights[end_block_x][end_block_z]) - (heights[end_block_x][start_block[z]])) > 2 or abs((heights[end_block_x][start_block[z]]) - start_block[y]) > 2):
                    x_distance = randint(4, 10)
                    z_divergence_diff = randint(-x_distance, x_distance)
                    end_block_x = (start_block[x] + (x_distance * x_modifier))
                    end_block_z = (start_block[z] + start_block[z] + z_divergence_diff)
                    if l == 1 or l == 3:
                        end_block_x = start_block[x] + z_divergence_diff
                        end_block_z = (start_block[z] + (x_distance * x_modifier))
                    if j == 99:
                        breakCheck = True
            
            #no suitable pathing available
            if breakCheck == True:
                break
            
            #set end block and intermediate block to go on height maps
            end_block = (end_block_x, heights[end_block_x][end_block_z], end_block_z)
            intermediate_block = (end_block[x], heights[end_block[x]][start_block[z]], start_block[z])

            #place down the starting, ending, and intermediate blocks
            place_corner(start_block)
            place_corner(intermediate_block)
            place_corner(end_block)

            #placex
            place_blocks_x(start_block, intermediate_block)

            #placez
            place_blocks_z(intermediate_block, end_block)

            second_start = (start_block[x] + 1, heights[start_block[x]][start_block[z] + 1], start_block[z] + 1)
            second_end = (end_block[x] + 1, heights[end_block[x]][end_block[z] + 1], end_block[z] + 1)
            second_intermediate = (second_end[x], heights[second_end[x]][second_start[z]], second_start[z])
            
            #place down the starting, ending, and intermediate blocks
            place_corner(second_start)
            place_corner(second_intermediate)
            place_corner(second_end)

            place_blocks_x(second_start, second_intermediate)
            place_blocks_z(second_intermediate, second_end)

            #temp
            #INTF.placeBlock(start_block[x], heights[start_block[x]][start_block[z]] - 1, start_block[z], "grass_path")
            #INTF.placeBlock(end_block[x], heights[end_block[x]][end_block[z]] - 1, end_block[z], "grass_path")
            #INTF.placeBlock(intermediate_block[x], heights[intermediate_block[x]][intermediate_block[z]] - 1, intermediate_block[z], "grass_path")

            print(heights)
            #reset start block in the same cardinal direction
            start_block = end_block
        
        #reset start block for new cardinal direction
        start_block = (path_start_x, heights[path_start_x][path_start_z], path_start_z)