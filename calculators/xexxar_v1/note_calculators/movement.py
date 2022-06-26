import math

def get_vector_length(object):
    return (object['mv'][0] ** 2 + object['mv'][1] ** 2) ** (1/2) / object['dt']

def calculate_movement_difficulty(object: dict, index, metadata: dict, objects: list):
    # strain = 0;
    #
    # i = index
    # while i > index - 8 and i > 1:
    #     strain += (get_vector_length(objects[i]) / (2 * metadata['cs_radius'])) * (1 / (1 + (index - i)))
    #     # strain += abs((get_vector_length(objects[i]) - get_vector_length(objects[i - 1])) / (2 * metadata['cs_radius'])) * (1 / (1 + (index - i)))
    #     i += -1

    return get_vector_length(object) / (2 * metadata['cs_radius'])
