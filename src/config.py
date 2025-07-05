import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

SQUARE = 60
SPHERE = 100
INITIAL_POS = (0, 0, -15)

INITIAL_ROTATIONS = 100

ANIMATION_TIME = 0.2

######################
## Scoring settings ##
######################
ALPHA = 0.65
BETA = 0.35

COLOR_MAP = {
    "white": (1, 1, 1),
    "red": (1, 0, 0),
    "blue": (0, 0, 1),
    "orange": (1, 0.5, 0),
    "green": (0, 1, 0),
    "yellow": (1, 1, 0),
}

NEIGHBORS = {
            # Each face maps to its neighbors in [up, right, down, left] order
            "white": ["green", "red", "blue", "orange"],
            "yellow": ["blue", "red", "green", "orange"],
            "red": ["white", "blue", "yellow", "green"],
            "orange": ["white", "green", "yellow", "blue"],
            "green": ["white", "orange", "yellow", "red"],
            "blue": ["white", "red", "yellow", "orange"]
        }