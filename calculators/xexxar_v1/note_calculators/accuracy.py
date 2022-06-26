import math

def dt_to_d(dt):
    dt = min(dt, 1000)
    return 0.5 + math.sin(math.pi * dt / 2000)

def calculate_accuracy_difficulty(object: dict, index, metadata: dict, objects: list):
    d = 0

    ## essentially, objects are harder to acc the slower they are.
    if object['type'] != 'spinner':
        if len(objects) > index + 1 and objects[index + 1]['type'] == 'circle':
            d = dt_to_d(object['dt'] - object['st']) / metadata['300_window'] ** 0.5
        else:
            d = dt_to_d(object['dt'] - object['st']) / metadata['50_window'] ** 0.5

    # Need to add complexity bonus for trick rhythms

    return d
