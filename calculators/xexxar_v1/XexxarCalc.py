import slider

from calculators import BaseCalculator
from helpers.gamemodes import GameMode
from helpers.Score import Score

class XexxarPerformanceCalculator(BaseCalculator.BaseCalculator):
    def __init__(self, beatmap_: slider.Beatmap, score_: Score, acc=None, mods_=None, tillerino=False, gameMode=GameMode.Standard):
        super().__init__(beatmap_, score_, acc, mods_, tillerino, gameMode)

    def calculate_pp(self):
        # Calculate the performance of the player
        # Here you have access to self.score and self.beatmap, which are the 2 main things
        # e.g. for every hitobject in the beatmap, print it out

        dt_enabled = self.score.mods & 64 > 0
        print(dt_enabled)

        for hitobject in self.beatmap.hit_objects(double_time=dt_enabled):
            # Depending on if you pass double_time, HR, ez etc. the hitobject here will already have its time + position updated
            # Its up to you to do the rest of the calculation, e.g. cirlesize, hitwindow etc.

            print(f"Hitobject is {hitobject.__class__.__name__} at {hitobject.position.x}:{hitobject.position.y} @ {hitobject.time}ms")
            pass
            

        self.pp = 420.69
        return self.pp