
class Score:
	__slots__ = ["scoreID", "playerName", "score", "maxCombo", "c50", "c100", "c300", "cMiss", "cKatu", "cGeki",
	             "fullCombo", "mods", "playerUserID","rank","date", "hasReplay", "fileMd5", "beatmap_id", "passed", "playDateTime",
	             "gameMode", "completed", "accuracy", "pp", "oldPersonalBest", "rankedScoreIncrease",
				 "_playTime", "_fullPlayTime", "quit", "failed"]
	def __init__(self):
		"""
		Initialize a (empty) score object.

		scoreID -- score ID, used to get score data from db. Optional.
		rank -- score rank. Optional
		setData -- if True, set score data from db using scoreID. Optional.
		"""
		self.scoreID = 0
		self.playerName = "nospe"
		self.score = 0
		self.maxCombo = 0
		self.c50 = 0
		self.c100 = 0
		self.c300 = 0
		self.cMiss = 0
		self.cKatu = 0
		self.cGeki = 0
		self.fullCombo = False
		self.mods = 0
		self.playerUserID = 0
		self.date = 0
		self.hasReplay = 0
		self.beatmap_id = 0

		self.fileMd5 = None
		self.passed = False
		self.playDateTime = 0
		self.gameMode = 0
		self.completed = 0

		self.accuracy = 0.00

		self.pp = 0.00

		self.oldPersonalBest = 0
		self.rankedScoreIncrease = 0

		self._playTime = None
		self._fullPlayTime = None
		self.quit = None
		self.failed = None

	def calculateAccuracy(self):
		"""
		Calculate and set accuracy for that score
		"""
		if self.gameMode == 0:
			# std
			totalPoints = self.c50*50+self.c100*100+self.c300*300
			totalHits = self.c300+self.c100+self.c50+self.cMiss
			if totalHits == 0:
				self.accuracy = 1
			else:
				self.accuracy = totalPoints/(totalHits*300)
		elif self.gameMode == 1:
			# taiko
			totalPoints = (self.c100*50)+(self.c300*100)
			totalHits = self.cMiss+self.c100+self.c300
			if totalHits == 0:
				self.accuracy = 1
			else:
				self.accuracy = totalPoints / (totalHits * 100)
		elif self.gameMode == 2:
			# ctb
			fruits = self.c300+self.c100+self.c50
			totalFruits = fruits+self.cMiss+self.cKatu
			if totalFruits == 0:
				self.accuracy = 1
			else:
				self.accuracy = fruits / totalFruits
		elif self.gameMode == 3:
			# mania
			totalPoints = self.c50*50+self.c100*100+self.cKatu*200+self.c300*300+self.cGeki*300
			totalHits = self.cMiss+self.c50+self.c100+self.c300+self.cGeki+self.cKatu
			self.accuracy = totalPoints / (totalHits * 300)
		else:
			# unknown gamemode
			self.accuracy = 0
