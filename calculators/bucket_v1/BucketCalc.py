import slider

from calculators import BaseCalculator
from helpers.gamemodes import GameMode
from helpers.Score import Score

class BucketPerformanceCalculator(BaseCalculator.BaseCalculator):
    def __init__(self, beatmap_: slider.Beatmap, score_: Score, acc=None, mods_=None, tillerino=False, gameMode=GameMode.Standard):
        super().__init__(beatmap_, score_, acc, mods_, tillerino, gameMode)

    def calculate_pp(self):
        dt_enabled = int(self.score.mods) & 64 > 0
        hr_enabled = int(self.score.mods) & 1 > 0
        ez_enabled = int(self.score.mods) & 2 > 0
        hd_enabled = int(self.score.mods) & 16 > 0
        ht_enabled = int(self.score.mods) & 32 > 0

        for hitobject in self.beatmap.hit_objects(double_time=dt_enabled, half_time=ht_enabled, hard_rock=hr_enabled, easy=ez_enabled):
            assert isinstance(hitobject, slider.beatmap.HitObject)
            # Depending on if you pass double_time, HR, ez etc. the hitobject here will already have its time + position updated
            # Its up to you to do the rest of the calculation, e.g. cirlesize, hitwindow etc.

            # print(f"Hitobject is {hitobject.__class__.__name__} at {hitobject.position.x}:{hitobject.position.y} @ {hitobject.time}ms")
            pass

        self.pp = 5
        return 5