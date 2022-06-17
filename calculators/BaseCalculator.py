# The interface to use in calculators

from abc import abstractmethod, ABCMeta

import slider
from helpers.Score import Score
from helpers.gamemodes import GameMode

class BaseCalculator(metaclass=ABCMeta):
    def __init__(self, beatmap_: slider.Beatmap, score_=Score, acc=None, mods_=None, tillerino=False, gameMode=GameMode.Standard):
        self.beatmap = beatmap_
        self.score = score_
        self.acc = acc
        self.mods = mods_
        self.tillerino = tillerino
        self.gameMode = gameMode
        
        self.perfects = 0
        self.oks = 0
        self.mehs = 0
        self.misses = 0

        self.stars = 0
        self.pp = self.calculate_pp()

    @abstractmethod
    def calculate_pp(self) -> float:
        pass
