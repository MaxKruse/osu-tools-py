import math

def calculate_movement_difficulty(object: dict, index, metadata: dict, objects: list):
    # return d/t for testing.

    return 0 #((object['mv'][0] / object['t']) ** 2 * (object['mv'][1] / object['t']) ** 2) ** (1/2)
