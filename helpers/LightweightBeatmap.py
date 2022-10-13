from dataclasses import dataclass


@dataclass
class LightweightBeatmap:
    beatmap_id: int
    display_name: int
    max_combo: int