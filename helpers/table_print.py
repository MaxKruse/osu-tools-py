from typing import Dict, List
import slider
from tabulate import tabulate

from helpers.Score import Score

def print_scores(old: Dict[int, Score], new: List[Score], maps: Dict[int, slider.Beatmap], toFile: str = ""):
    """
    Prints the scores in a table.
    """

    headers = ["Beatmap ID", "Beatmap Name", "Combo", "Accuracy", "PP Before", "PP After", "Change"]
    toPrint = []

    for newScore in new:
        s1: Score = old[newScore.beatmap_id]
        s2: Score = newScore

        # Calc the acc
        s1.calculateAccuracy()
        m: slider.Beatmap = maps[s1.beatmap_id]

        toPrint.append([
            s1.beatmap_id,
            m.display_name,
            f"{s1.maxCombo}/{m.max_combo}x",
            f"{(float(s1.accuracy)*100.0):.2f}%",
            f"{float(s1.pp):.3f}pp",
            f"{float(s2.pp):.3f}pp",
            f"{(float(s2.pp) - float(s1.pp)):.3f}"
        ])

    resStr = tabulate(toPrint, headers=headers, tablefmt="grid", showindex=True)
    
    if toFile == "":
        print(resStr)
    else:
        with open(toFile, "w") as f:
            f.write(resStr)
    