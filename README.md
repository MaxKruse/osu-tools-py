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