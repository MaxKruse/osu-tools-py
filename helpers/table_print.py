from typing import Dict, List
from prettytable import PrettyTable
import slider

from helpers.Score import Score

__maxLength = 80

def print_scores(old: Dict[int, Score], new: List[Score], maps: Dict[int, slider.Beatmap], toFile: str = ""):
    """
    Prints the scores in a table.
    """

    # Setup the printer
    printer = PrettyTable()

    headers = ["Beatmap ID", "Beatmap Name", "Combo", "Accuracy", "PP Before", "PP After", "Change"]
    printer.field_names = headers

    printer.border = True
    printer.float_format = ".3"
    printer.align["Change"] = "r"   
    printer.align["Beatmap ID"] = "r"


    for newScore in new:
        s1: Score = old[newScore.beatmap_id]
        s2: Score = newScore

        # Calc the acc
        s1.calculateAccuracy()
        m: slider.Beatmap = maps[s1.beatmap_id]

        printer.add_row([
            s1.beatmap_id,
            (m.display_name[:__maxLength] + "..") if len(m.display_name) > __maxLength else m.display_name,
            f"{s1.maxCombo}/{m.max_combo}x",
            f"{(float(s1.accuracy)*100.0):.2f}%",
            f"{float(s1.pp):.3f}pp",
            f"{float(s2.pp):.3f}pp",
            f"{(float(s2.pp) - float(s1.pp)):.3f}"
        ])
    
    print(printer)

    if toFile != "":
        with open(toFile, "w") as f:
            f.write(printer.get_json_string())