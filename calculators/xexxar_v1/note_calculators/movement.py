import math

def get_vector_length(object):
    return (object['mv'][0] ** 2 + object['mv'][1] ** 2) ** (1/2) / object['dt']

def object_add(object1, object2):
    object = {}
    object['dt'] = max(object1['dt'], object2['dt'])
    object['mv'] = [object1['mv'][0] + object2['mv'][0], object1['mv'][1] + object2['mv'][1]]
    return object

def object_scale(object, scalar):
    o = {}
    o['dt'] = object['dt']
    o['mv'] = [object['mv'][0] * scalar, object['mv'][1] * scalar]
    return o

def calculate_movement_difficulty(object: dict, index, metadata: dict, objects: list):
    angleBonusMultiplier = 2.0
    velChangeMultiplier = 3.0

    difficulty = 0

    if index > 0:
        prev_object = objects[index - 1]
        diff_vector = max(0, min(get_vector_length(object_add(object, prev_object)) - max(get_vector_length(prev_object),
                                                                                                       get_vector_length(object)),
                                 get_vector_length(object_add(object, object_scale(prev_object, -1))) - max(get_vector_length(prev_object),
                                                                                                                         get_vector_length(object))))
        difficulty += angleBonusMultiplier * diff_vector / (2 * metadata['cs_radius'])

        difference = min(get_vector_length(object), max(0, get_vector_length(prev_object) - get_vector_length(object) - max(get_vector_length(prev_object), get_vector_length(object)) / 4))

        if (object['dt'] - prev_object['dt'] < 10):
            difficulty += velChangeMultiplier * difference / (2 * metadata['cs_radius'])

    difficulty += get_vector_length(object) / (2 * metadata['cs_radius'])

    return difficulty
