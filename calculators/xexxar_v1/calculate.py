# Imports
import logging
import math
from calculators.xexxar_v1.note_calculators.accuracy import calculate_accuracy_difficulty
from calculators.xexxar_v1.note_calculators.movement import calculate_movement_difficulty
from calculators.xexxar_v1.note_calculators.slider import calculate_slider_difficulty
from calculators.xexxar_v1.note_calculators.tap import calculate_tap_difficulty

# import pprint
#
# pp = pprint.PrettyPrinter(indent=1)
# pp.pprint([

def vectorize_map_data(map_data: list):
    out = []

    for index, object in enumerate(map_data):
        if index < len(map_data) - 1:
            o = {}

            if object['type'] == 'slider': # If I'm a slider.
                slider_ticks = iter(object['S'])

                S = []

                for i, tick in enumerate(object['S']):
                    if i < len(object['S']) - 1:
                        S.append({'dt': object['S'][i + 1]['t'] - tick['t'],
                                  'mv': [object['S'][i + 1]['x'] - tick['x'], object['S'][i + 1]['y'] - tick['y']]})

                o['S'] = S
                o['type'] = 'slider'
                o['mv'] = [map_data[index + 1]['x'] - object['S'][-1]['x'], map_data[index + 1]['y'] - object['S'][-1]['y']] # the vector of movement from tail to next head
                o['mt'] = map_data[index + 1]['t'] - object['end_t'] # the time from slider end to next object
                o['dt'] = map_data[index + 1]['t'] - object['t'] # the time from slider head to next object
                o['st'] = object['end_t'] - object['t'] # the time from slidr head to slider tail
                o['t'] = object['t'] # the raw start time of the object

            elif object['type'] == 'spinner': # If I'm a spinner.
                o['type'] = 'spinner'
            else:
                o['type'] = 'circle'

            o['mv'] = [map_data[index + 1]['x'] - object['x'], map_data[index + 1]['y'] - object['y']] # the vector of movement
            o['dt'] = map_data[index + 1]['t'] - object['t'] # the time from object to next object
            o['st'] = 0
            o['t'] = object['t'] # the raw start time of the object

            out.append(o)

    return out


def create_difficulty_metadata(metadata: dict):
    ar_window = 0
    if metadata['AR'] > 5:
        ar_window = 1200 - 750 * (metadata['AR'] - 5) / 5
    else:
        ar_window = 1200 + 600 * (5 - metadata['AR']) / 5

    return {'300_window': 80 - 6 * metadata['OD'],
            '100_window': 140 - 8 * metadata['OD'],
            '50_window': 200 - 10 * metadata['OD'],
            'ar_window': ar_window,
            'cs_radius': 54.4 - 4.48 * metadata['CS'],
            'cs_area': math.pi * 54.4 - 4.48 * metadata['CS'] ** 2}


def calculate_note_difficulties(metadata: dict, objects: list):
    out = []

    tap_multiplier = 12.5
    acc_multiplier = 10
    sli_multiplier = 1
    mov_multiplier = 60

    for index, object, in enumerate(objects):
        # call off to every sub model and calculate the difficulty for this given object and index.
        o = {'t': object['t']}

        o['ad'] = acc_multiplier * calculate_accuracy_difficulty(object, index, metadata, objects) # refers to the difficulty to acc this note with a 300.
        o['md'] = mov_multiplier * calculate_movement_difficulty(object, index, metadata, objects) # refers to the difficulty to aim this note.
        o['sd'] = sli_multiplier * calculate_slider_difficulty(object, index, metadata, objects) # refers to the difficulty to not drop combo on this note
        o['td'] = tap_multiplier * calculate_tap_difficulty(object, index, metadata, objects) # refers to the difficulty to tap this note

        out.append(o)

    return out


def lp_sum(vector: list, p):
    sum = 0

    for x in vector:
        sum += x ** p
    sum = sum ** (1 / p)

    return sum


def apply_score_judgements(note_difficulties: list, score_data: dict):
    out = []

    note_difficulties.sort(reverse=True, key=lambda note: lp_sum([note['ad'], note['md'], note['sd'], note['td']], 1.1))

    object_count = len(note_difficulties)

    misses = 5 * score_data['Misses']#int(object_count * min(1, score_data['Misses']) / (0.05 * object_count))
    hundreds = score_data['100'] #int(object_count - object_count * (.95 ** ((100 * score_data['100']) / object_count)))
    fifties = score_data['50'] #int(object_count - object_count * (.9 ** ((100 * score_data['50']) / object_count)))

    # print(hundreds)

    for note in note_difficulties:
        if misses > 0:
            note['ad'] = 0
            note['md'] = 0
            note['sd'] = 0
            note['td'] = 0

            out.append(note)
            misses = misses - 1
        elif fifties > 0:
            note['ad'] = 0
            note['md'] = note['md']
            note['sd'] = note['sd']
            note['td'] = 0

            out.append(note)
            fifties = fifties - 1
        elif hundreds > 0:
            note['ad'] = 0
            note['md'] = note['md']
            note['sd'] = note['sd']
            note['td'] = note['td']

            out.append(note)
            hundreds = hundreds - 1
        else:
            out.append(note)

    return out


def calculate(metadata: dict, map_data: list, score_data: dict):
    # Entry point to calculate the PP value for a given set of map data and score information.

    ### Values for p derivation for lp sum.
    difficulty_doubling_rate = 1.0625
    p = 1.0 / math.log(difficulty_doubling_rate, 2)
    pp_multiplier = 1.5

    # Map data is currently in a raw format, we want to transform it into a vectorized format. remember to store raw time. might be useful.
    objects = vectorize_map_data(map_data)
    difficulty_metadata = create_difficulty_metadata(metadata)

    # Now that we have vectorized hit judgements, we can calculate the difficulty of every object. broken up into judgement form.
    note_difficulties = calculate_note_difficulties(difficulty_metadata, objects)

    ## Apply penalties to score based off score data
    note_difficulties = apply_score_judgements(note_difficulties, score_data)

    # Calculate effective Star Rating.
    star_rating = 0

    for note in note_difficulties:
        star_rating += lp_sum([note['ad'], note['md'], note['sd'], note['td']], 1.1) ** p

    star_rating = star_rating ** (1/p)

    ## Apply a % nerf to

    pp = pp_multiplier * star_rating ** 3 # 3 here cubes this SR into a pp value. pp_multiplier is a scalar to adjust things.

    # logging.debug("Star Rating: ", star_rating)
    # combo game.
    pp *= 0.5 + 0.5 * (score_data['ScoreCombo'] / metadata['MaxCombo'])

    return pp #result
