import slider

from calculators import BaseCalculator
from helpers.gamemodes import GameMode
from helpers.Score import Score
from calculators.xexxar_v1.calculate import calculate

class XexxarPerformanceCalculator(BaseCalculator.BaseCalculator):
    def __init__(self, beatmap_: slider.Beatmap, score_: Score, acc=None, mods_=None, tillerino=False, gameMode=GameMode.Standard):
        super().__init__(beatmap_, score_, acc, mods_, tillerino, gameMode)

    def calculate_pp(self):
        # Calculate the performance of the player
        # Here you have access to self.score and self.beatmap, which are the 2 main things
        # e.g. for every hitobject in the beatmap, print it out

        # Make sure you cast the mods. This is python...
        dt_enabled = int(self.score.mods) & 64 > 0
        # print(f"DT Enabled? {'yes' if dt_enabled else 'no'}")

        for hitobject in self.beatmap.hit_objects(double_time=dt_enabled):
            assert isinstance(hitobject, slider.beatmap.HitObject) # After this, intellisense will work
            # Depending on if you pass double_time, HR, ez etc. the hitobject here will already have its time + position updated
            # Its up to you to do the rest of the calculation, e.g. cirlesize, hitwindow etc.

            # print(f"Hitobject is {hitobject.__class__.__name__} at {hitobject.position.x}:{hitobject.position.y} @ {hitobject.time}ms")
            pass

        # someone, or me, needs to do some magic to put the data into the format I'm going for here.
        # I don't really want to do it cause I'm lazy and the engine itself is gonna be complex
        # so if I can pawn off that work that'd be hype. I'd love that for me.
        # here is the data format we need.

        # calculate({'AR': ar,
        #           'CS': cs,
        #           'HP': lol,
        #           'OD': od,
        #           'CircleCount': circleCount,
        #           'SliderCount': sliderCount,
        #           'SpinnerCount': lol2,
        #           'MaxCombo': maxCombo,}, #anything else i'm not thinking of.
        #          [{'dx': x,
        #            'dy': y,
        #            'dt': t,
        #            'S': None}
        #           {'dx': x,
        #            'dy': y,
        #            'dt': t,
        #            'S': [{'dx': x, #movement required to reach center of tick or repeat
        #                   'dy': y,
        #                   'dt': t}
        #                   .., #for how every many ticks or repeats there
        #                  {'dx': x, #distance to 'lazy slider end' center
        #                   'dy': y,
        #                   'dt': t}]}
        #            ..,
        #           {'dx': x,
        #            'dy': y,
        #            'dt': t,},
        #          {'300': threehundreds,
        #           '100': onehundreds,
        #           '50': fiftys,
        #           'Misses': misses,
        #           'ScoreCombo': combo}) #anything else I'm not thinking of.


        self.pp = calculate({}, [], {},)
        return self.pp
