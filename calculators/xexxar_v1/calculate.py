# Imports
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

    tap_multiplier = 15
    acc_multiplier = 60
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
    #
    # ### NOTE Coming out this method, we have the following structure
    #
    # [{'m'  # Store the movement difficulty.
    #   'a'  # Store the raw accuracy difficulty
    #   's'  # Store the raw speed difficulty
    #   'c'} # Store the slider end difficulty
    #   ...]
    #
    # # This will be used against the judgements from the map to derive penalties based off score data.
    #
    # # Combo scaling: (dropped sliders)
    # # for FC plays, we drop 'c' difficulty based off the number of dropped slider ends (based off missing combo).
    # # for non FC plays, we do the same thing, so since combo is missing, we're able to derive the number of misses.
    #
    # # Miss Scaling:
    # # entire note is removed from calculation (and additional notes I'm assuming, based on penalty).
    #
    # # 100 Scaling:
    # # Remove the 'a' difficulty from the strains and 25% of the speed 's' strain.
    #
    # # 50 Scaling:
    # # Remove the 'a' difficulty and the 's' difficulty from the strain.
    #
    # ### NOTE end
    #
    # ## Apply penalties to score based off
    # note_difficulties = apply_score_judgements(note_difficulties, score_data)
    #
    # Calculate effective Star Rating.
    star_rating = 0

    for note in note_difficulties:
        star_rating += (note['ad'] + note['md'] + note['sd'] + note['td']) ** p

    star_rating = star_rating ** (1/p)

    ## Apply a % nerf to

    pp = pp_multiplier * star_rating ** 3 # 3 here cubes this SR into a pp value. pp_multiplier is a scalar to adjust things.

    # combo game.
    # pp *= 0.75 + 0.25 * (score_data['ScoreCombo'] / metadata['MaxCombo'])

    return pp #result
