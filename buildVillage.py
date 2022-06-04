from pathing import create_path
from gdpc import interface as INTF

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

if __name__ == "__main__":
    #args -> xcoord of start block, ycoord of start block, iterations per path, path min, path max
    """
    -paths can be thought of as a bunch of repeating "L's"
    -iterations are the number of L's per path
    -path min and path max set the bounds for the smallest/largest longitudinal/latitudal L
    -a path of 10 iterations with a min of 1 and a max of 4 will create 10 connecting L's of
        varying size; some will be just 1 block, some a 2 block L, some a 3 block L
    -if the path goes out of play area it crashes
    """
    create_path(STARTX + 74, STARTZ + 71, 5, 4, 10)