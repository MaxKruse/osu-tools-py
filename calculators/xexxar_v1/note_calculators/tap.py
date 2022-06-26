import math

def calculate_tap_difficulty(object: dict, index, metadata: dict, objects: list):
    strain = 0;

    i = index
    while i > index - 32 or i > 0:
        strain += 1 / objects[i]['dt'] * (4 / (4 + (index - i)))
        i += -1

    return strain
