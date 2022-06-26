import math

def calculate_tap_difficulty(object: dict, index, metadata: dict, objects: list):
    strain = 0;

    i = index
    while i > 0 and object['t'] - objects[i]['t'] < 5000:
        strain += max(0, 1 - (object['t'] - objects[i]['t']) / 5000) / 75 #arbitrary / 75 here for easier maths.
        i += -1

    return strain
