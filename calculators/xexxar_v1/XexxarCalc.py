import slider

from calculators import BaseCalculator
from helpers.gamemodes import GameMode
from helpers.Score import Score
from calculators.xexxar_v1.calculate import calculate
from helpers.time_convert import timedelta_to_ms

class XexxarPerformanceCalculator(BaseCalculator.BaseCalculator):
    def __init__(self, beatmap_: slider.Beatmap, score_: Score, acc=None, mods_=None, tillerino=False, gameMode=GameMode.Standard):
        super().__init__(beatmap_, score_, acc, mods_, tillerino, gameMode)

    def calculate_pp(self):
        # Calculate the performance of the player
        # Here you have access to self.score and self.beatmap, which are the 2 main things
        # e.g. for every hitobject in the beatmap, print it out

        dt_enabled = int(self.score.mods) & 64 > 0
        hr_enabled = int(self.score.mods) & 1 > 0
        ez_enabled = int(self.score.mods) & 2 > 0
        hd_enabled = int(self.score.mods) & 16 > 0
        ht_enabled = int(self.score.mods) & 32 > 0

        cachedHitobjects = self.beatmap.hit_objects(double_time=dt_enabled, half_time=ht_enabled, hard_rock=hr_enabled, easy=ez_enabled)

        # form the 3 lists/dicts xexxar wants for calculate.py
        metadata = {
            'AR': self.beatmap.ar(double_time=dt_enabled, half_time=ht_enabled, hard_rock=hr_enabled, easy=ez_enabled),
            'CS': self.beatmap.cs(hard_rock=hr_enabled, easy=ez_enabled),
            'HP': self.beatmap.hp(hard_rock=hr_enabled, easy=ez_enabled),
            'OD': self.beatmap.od(double_time=dt_enabled, half_time=ht_enabled, hard_rock=hr_enabled, easy=ez_enabled),
            'CircleCount': 0,
            'SliderCount': 0,
            'SpinnerCount': 0,
            'MaxCombo': self.beatmap.max_combo
        }

        scoredata = {
            '300': self.score.c300,
            '100': self.score.c100,
            '50': self.score.c50,
            'Misses': self.score.cMiss,
            'ScoreCombo': self.score.maxCombo
        }

        mapdata = []

        for hitobject in cachedHitobjects:
            assert isinstance(hitobject, slider.beatmap.HitObject) # After this, intellisense will work
            # Depending on if you pass double_time, HR, ez etc. the hitobject here will already have its time + position updated
            # Its up to you to do the rest of the calculation, e.g. cirlesize, hitwindow etc.

            if isinstance(hitobject, slider.beatmap.Circle):
                metadata['CircleCount'] += 1

                mapdata.append({
                    "type": "circle",
                    "x": hitobject.position.x,
                    "y": hitobject.position.y,
                    "t": timedelta_to_ms(hitobject.time)
                })

            elif isinstance(hitobject, slider.beatmap.Slider):
                metadata['SliderCount'] += 1

                sliderPoints = []

                assert isinstance(hitobject, slider.beatmap.Slider)

                for point in hitobject.tick_points:
                    sliderPoints.append({
                        "x": point.x,
                        "y": point.y,
                        "t": timedelta_to_ms(point.offset),
                        "type": "tick"
                    })

                mapdata.append({
                    "type": "slider",
                    "x": hitobject.position.x,
                    "y": hitobject.position.y,
                    "t": timedelta_to_ms(hitobject.time),
                    "S": sliderPoints
                })

            elif isinstance(hitobject, slider.beatmap.Spinner):
                metadata['SpinnerCount'] += 1

                mapdata.append({
                    "type": "spinner",
                    "x": hitobject.position.x,
                    "y": hitobject.position.y,
                    "t": hitobject.time
                })
            
            pass



        # someone, or me, needs to do some magic to put the data into the format I'm going for here.
        # I don't really want to do it cause I'm lazy and the engine itself is gonna be complex
        # so if I can pawn off that work that'd be hype. I'd love that for me.
        # here is the data format we need.

        self.pp = calculate(metadata=metadata, map_data=mapdata, score_data=scoredata)
        return self.pp
