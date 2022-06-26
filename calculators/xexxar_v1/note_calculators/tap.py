import math

def calculate_tap_difficulty(object: dict, index, metadata: dict, objects: list):
    strain = 0;

    i = index
    while i > index - 32 and i > 0:
        strain += 1 / objects[i]['dt'] * (1 / (1 + (index - i)))
        i += -1

    return strain
