# Osu Tools Python

Small python osu-tools version, for rapidly developing pp systems.

Using [slider](https://pypi.org/project/slider/) to parse osu files.

## Installation

    pip install -r requirements.txt

## Usage

    python .\main.py profile osu 1955

## Development

To develop a new pp calculator, follow the steps below.

1. Create a new folder in the `calculators` folder.
2. Create a `__init__.py` file in the folder.
3. Name your calculator in that folder, e.g. `MyCalc.py`. Make sure you inherit `BaseCalculator` and only customize `calculate_pp`. An example is in `XexxarCalc.py`
4. In `calculators/__init__.py`, add your calculator to the `calculators` list by giving it a name and the class name.

Thats it. You can now call your calculator by providing the `--calculator` flag, e.g. ` python .\main.py --calculator MyCalc file --beatmap .\osu_files\2520047.osu`.

## Xexxar pp

Xexxar's PP calc currently differentiates the following skills:

1. Movement Distance
2. Movement Velocity
3. Distance Difference between Objects (e.g. changing spacing)
4. Angle Calculation (0, 45, 90, 135, 180)
5. Visual Density (+ HD)
6. Visual Distance (+ HD)
7. Slider Velocity
8. Slider Leniency
9. Tap Density
10. Tap Stamina
11. Accuracy Window
12. Beatsnap/Rhythm Changes (1/2->1/4, 3/4->1/4, 1/2->1/3)
13. Reading: Overlaps
14. Acc on slow parts
15. Slider Movement Requirement
16. Slider Complexity (Visual)
17. Difficulty Curve
