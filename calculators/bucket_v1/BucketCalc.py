from datetime import timedelta
from itertools import accumulate
import math
from typing import List
import numpy as np
import slider

from calculators import BaseCalculator
from helpers.gamemodes import GameMode
from helpers.Score import Score

class BucketPerformanceCalculator(BaseCalculator.BaseCalculator):
    def __init__(self, beatmap_: slider.Beatmap, score_: Score, acc=None, mods_=None, tillerino=False, gameMode=GameMode.Standard):
        self.max_time_difference = 500 # Clamp so that objects > 500ms are not fucking up the calc
        self.min_angle_consideration = 60.0 # inner angle between N points
        self.max_angle_consideration = 120.0 # outer angle between N points
        self.bucket_size = 10 # Can be adjusted using self.set_bucket(N)
        super().__init__(beatmap_, score_, acc, mods_, tillerino, gameMode)

    def set_bucket(self, bucket_size):
        # check if the bucket is > 3
        if bucket_size < 4:
            raise ValueError("Bucket size must be > 3")

        # check if the bucket is smaller than the total number of hitobjects / 2
        if bucket_size > len(self.beatmap.hit_objects()) / 2:
            raise ValueError("Bucket size must be smaller than the total number of hitobjects / 2")

        self.bucket_size = bucket_size

    def calculate_pp(self):
        self.pp = 1.0
        return self.pp
        dt_enabled = int(self.score.mods) & 64 > 0
        hr_enabled = int(self.score.mods) & 1 > 0
        ez_enabled = int(self.score.mods) & 2 > 0
        hd_enabled = int(self.score.mods) & 16 > 0
        ht_enabled = int(self.score.mods) & 32 > 0

        cachedHitobjects = self.beatmap.hit_objects(double_time=dt_enabled, half_time=ht_enabled, hard_rock=hr_enabled, easy=ez_enabled)

        bucket_values = []

        # iterate over all hitobjects, using the bucketsize
        for i in range(0, len(cachedHitobjects) - self.bucket_size):

            # Grab the next bucket of hitobjects
            # make sure that we don't go out of bounds
            if i + self.bucket_size > len(cachedHitobjects):
                bucket = cachedHitobjects[i:]
            else:
                bucket = cachedHitobjects[i:i+self.bucket_size]

            bucket_values.append(self.calculate_bucket_value(bucket))
            
            # get the angle between
            pass
        
        res = 0.0

        # for every value in bucket_values, calculate the difference between the next value and the current value
        # the difference is abs()
        # then add the difference to the res
        for i in range(0, len(bucket_values) - 1):
            res += abs(bucket_values[i] - bucket_values[i+1])

        self.pp = res

        return self.pp

    def calculate_bucket_value(self, bucket):
        # calculate the bucket value
        
        angle_values = self.angle_calc(bucket)
        strain_values = self.strain_calc(bucket)
        res = sum(angle_values) + sum(strain_values)

        return res

    def strain_calc(self, bucket):
        strain_values = [1.0]
        return strain_values


    def angle_calc(self, bucket):
        angle_values = [0.0] # start with a 0.0 score to avoid farm maps giving literally no bonus here

        # Angle calc first
        for i in range(0, len(bucket) - 3):
            hitobject1 = bucket[i]
            hitobject2 = bucket[i+1]
            hitobject3 = bucket[i+2]
            assert isinstance(hitobject1, slider.beatmap.HitObject)
            assert isinstance(hitobject2, slider.beatmap.HitObject)
            assert isinstance(hitobject3, slider.beatmap.HitObject)
            pos1 = hitobject1.position
            pos2 = hitobject2.position
            pos3 = hitobject3.position

            positions = []
            times = []

            positions.append(pos1)
            times.append(hitobject1.time)
            positions.append(pos2)
            times.append(hitobject2.time)

            # if pos3 is a slider, calculate the angles based on all sliderticks if there are more than 3
            if isinstance(hitobject3, slider.beatmap.Slider):
                if len(hitobject3.tick_points) > 2:
                    positions = []
                    times = []

                    positions.append(hitobject3.position)
                    times.append(hitobject3.time)

                    for tick in hitobject3.tick_points:
                        positions.append(slider.Position(tick.x, tick.y))
                        times.append(tick.offset)
                else:
                    positions.append(pos3)
                    times.append(hitobject3.time)
            else:
                positions.append(pos3)
                times.append(hitobject3.time)
            
            assert len(positions) == len(times)
            assert len(positions) >= 3, "There must be at least 3 positions to calculate an angle"
        
            angle_values += self.angle_array_calc(positions, times)
            
        return angle_values

    def angle_array_calc(self, position_array: List[slider.Position], times: List[timedelta]):
        angle_values = []
        # go through the position array in chunks of 3
        for i in range(0, len(position_array) - 3):
            pos1 = position_array[i]
            pos2 = position_array[i+1]
            pos3 = position_array[i+2]
 
            time2 = times[i+1]
            time3 = times[i+2]

            # if all 3 hitobjects are circles, continue as normal
            assert isinstance(pos1, slider.beatmap.Position)
            assert isinstance(pos2, slider.beatmap.Position)
            assert isinstance(pos3, slider.beatmap.Position)

            angle = get_angle(pos1, pos2, pos3)

            assert angle >= 0, f"On beatmap {self.beatmap.beatmap_id} @ {pos1} {time2}ms, Angle is negative: {angle}"
            

            # if the angle is under our threshhold to consider it, dont add anything for it
            if angle < self.min_angle_consideration:
                continue

            # if the angle is over our threshhold to consider it, clamp it to our max angle
            if angle > self.max_angle_consideration:
                angle = self.max_angle_consideration

            # depending how far away the angle is from our max, give it a score
            angle_score = self.angle_score(angle)
            # depending on the timedifference between the 3 hitobjects, give it a multiplier
            timedifference = time3 - time2 # type: timedelta
            timedifference = timedifference if timedifference <= timedelta(milliseconds=self.max_time_difference) else timedelta(milliseconds=self.max_time_difference)
            
            timedifference_score = (timedifference.microseconds / 1000.0) / self.max_time_difference

            # the lower the timedifference is, the higher the score is
            # the higher the angle is, the higher the score is
            
            # multiply the angle score by the timedifference score
            angle_score = angle_score ** timedifference_score
            angle_values.append(angle_score)

        return angle_values

    def angle_score(self, angle: float):
        # calculate the score for the angle
        # the score is the angle divided by the max angle
        # then we give it an exponential curve, using eulers number
        resFraction = angle / self.max_angle_consideration
        res = resFraction**math.e
        res = res**0.7 # lessen the curve
        return res

def get_angle(point_1: slider.beatmap.Position, point_2: slider.beatmap.Position, point_3: slider.beatmap.Position): #These can also be four parameters instead of two arrays
    
    arr1 = np.array([point_1.x, point_1.y])
    arr2 = np.array([point_2.x, point_2.y])
    arr3 = np.array([point_3.x, point_3.y])

    ba = arr1 - arr2
    bc = arr3 - arr2

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    res = np.degrees(angle)

    # if res is nan, return 0
    if math.isnan(res):
        return 0
    return res