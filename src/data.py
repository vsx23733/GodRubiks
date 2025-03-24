# -*- coding: utf-8 -*-
"""
Created on Sat Dec  21 16:31:38 2024

@author: Axel
"""
# U : W
# D : Y
# F : B
# B : G
# L : R 
# R : O

# RGB Colors
WHITE = (1, 1, 1)
YELLOW = (1, 1, 0)
BLUE = (0, 0, 1)
GREEN = (0, 1, 0)
ORANGE = (1, 0.5, 0)
RED = (1, 0, 0)
BLACK = (0, 0, 0)
color_list = [WHITE, YELLOW, ORANGE, BLUE, RED, GREEN]

center_list = ["U", "D", "R", "F", "L", "B"]
corner_list = ["URF", "UFL", "ULB", "UBR", "DFR", "DLF", "DBL", "DRB"]
arete_list = ["UF", "UR", "UB", "UL", "DF", "DR", "DB", "DL", "FR", "FL", "BL", "BR"]


# def fact(n):
#     """ Return n! """
#     return 1 if n in (0,1) else n*fact(n-1)
fact = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800]


arete_permutations = {'U': [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
                       'D': [0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11],
                       'F': [0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11],
                       'B': [0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7],
                       'L': [0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11],
                       'R': [8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0]}

corner_permutations = {'U': [3, 0, 1, 2, 4, 5, 6, 7],
                      'D': [0, 1, 2, 3, 5, 6, 7, 4],
                      'F': [1, 5, 2, 3, 0, 4, 6, 7],
                      'B': [0, 1, 3, 7, 4, 5, 2, 6],
                      'L': [0, 2, 6, 3, 4, 1, 5, 7],
                      'R': [4, 1, 2, 0, 7, 5, 6, 3]}

aretes_orientations = {'U': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       'D': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       'F': [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
                       'B': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
                       'L': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       'R': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

corner_orientations = {'U': [0, 0, 0, 0, 0, 0, 0, 0],
                      'D': [0, 0, 0, 0, 0, 0, 0, 0],
                      'F': [1, 2, 0, 0, 2, 1, 0, 0],
                      'B': [0, 0, 1, 2, 0, 0, 2, 1],
                      'L': [0, 1, 2, 0, 0, 2, 1, 0],
                      'R': [2, 0, 0, 1, 1, 0, 0, 2]}

###################################
### Data for 3D Visualization ###
###################################


# Table showing the axis of rotation as a function of the rotation performed,
# if you rotate counter-clockwise, multiply the axis by -1

rotation_axe = {'U': (0, -1, 0), 'F': (0, 0, -1), 'R': (-1, 0, 0),
                'D': (0, 1, 0), 'B': (0, 0, 1), 'L': (1, 0, 0)}


# Table of coordinates for tracing the surface that will conceal the cube's interior during face rotation

hide_coords = {'U': [(-3, 1, -3), (3, 1, -3), (3, 1, 3), (-3, 1, 3)],
               'D': [(-3, -1, -3), (3, -1, -3), (3, -1, 3), (-3, -1, 3)],
               'F': [(-3, 3, 1), (-3, -3, 1), (3, -3, 1), (3, 3, 1)],
               'B': [(-3, 3, -1), (-3, -3, -1), (3, -3, -1), (3, 3, -1)],
               'L': [(-1, 3, -3), (-1, -3, -3), (-1, -3, 3), (-1, 3, 3)],
               'R': [(1, 3, -3), (1, -3, -3), (1, -3, 3), (1, 3, 3)]}


# List of points for adjusting texture on surface
texMap = [(0, 0), (0, 1), (1, 1), (1, 0)]

# Coordinates of the 8 points used to draw a cube in space
s = [(1, 1, 1), (-1, 1, 1), (-1, 1, -1), (1, 1, -1),
     (1, -1, 1), (-1, -1, 1), (-1, -1, -1), (1, -1, -1)]

# Function to change cube size
peaks = lambda x: [list(map(float.__mul__, [x] * 3, point)) for point in s]

indices = [(0, 1, 2, 3), (4, 5, 6, 7), (7, 4, 0, 3), (4, 5, 1, 0), (5, 6, 2, 1), (6, 7, 3, 2)]

position_list = ['F', 'L', 'D', 'U', 'R', 'B',
                   'DR', 'UB', 'FL', 'BL',
                   'DF', 'UR', 'UL', 'DB',
                   'DL', 'UF', 'FR', 'BR',
                   'UBR', 'UFR', 'UFL', 'DFR',
                   'DFL', 'UBL', 'DBL', 'DBR']

table_positions_centers = [(0, 2, 0), (0, -2, 0), (2, 0, 0),
                           (0, 0, 2), (-2, 0, 0), (0, 0, -2)]

table_positions_arete = [(2, 2, 0), (0, 2, 2), (-2, 2, 0), (0, 2, -2),
                          (2, -2, 0), (0, -2, 2), (-2, -2, 0), (0, -2, -2),
                          (2, 0, 2), (-2, 0, 2), (-2, 0, -2), (2, 0, -2)]

table_positions_corners = [(2, 2, 2), (-2, 2, 2), (-2, 2, -2), (2, 2, -2),
                         (2, -2, 2), (-2, -2, 2), (-2, -2, -2), (2, -2, -2)]

table_colors_centers = [[0], [1], [2], [3], [4], [5]]

table_colors_aretes = [[0, 2], [0, 3], [0, 4], [0, 5],
                         [1, 2], [1, 3], [1, 4], [1, 5],
                         [3, 2], [3, 4], [5, 4], [5, 2]]

table_colors_corners = [[0, 2, 3], [0, 3, 4], [0, 4, 5], [0, 5, 2],
                        [1, 3, 2], [1, 4, 3], [1, 5, 4], [1, 2, 5]]

table_axeOrientation_aretes = [(1, 1, 0), (0, 1, 1), (-1, 1, 0), (0, 1, -1),
                               (1, -1, 0), (0, -1, 1), (-1, -1, 0), (0, -1, -1),
                               (1, 0, 1), (-1, 0, 1), (-1, 0, -1), (1, 0, -1)]

table_axeOrientation_corners = [(1, 1, 1), (-1, 1, 1), (-1, 1, -1), (1, 1, -1),
                              (1, -1, 1), (-1, -1, 1), (-1, -1, -1), (1, -1, -1)]

# Table of facets that must display a color for each part

table_colors = {'U': [0], 'D': [1], 'R': [2],
                  'F': [3], 'L': [4], 'B': [5],
                  'UR': [0, 2], 'UF': [0, 3], 'UL': [0, 4], 'UB': [0, 5],
                  'DR': [1, 2], 'DF': [1, 3], 'DL': [1, 4], 'DB': [1, 5],
                  'FR': [3, 2], 'FL': [3, 4], 'BL': [5, 4], 'BR': [5, 2],
                  'URF': [0, 2, 3], 'UFL': [0, 3, 4],
                  'ULB': [0, 4, 5], 'UBR': [0, 5, 2],
                  'DFR': [1, 3, 2], 'DLF': [1, 4, 3],
                  'DBL': [1, 5, 4], 'DRB': [1, 2, 5]}

# Table (dX, dY, dZ)
# Translation parameters for positioning parts in space relative to cube center

table_positions = {'': (0, 0, 0),
                   'U': (0, 2, 0), 'D': (0, -2, 0), 'F': (0, 0, 2),
                   'B': (0, 0, -2), 'L': (-2, 0, 0), 'R': (2, 0, 0),
                   'UF': (0, 2, 2), 'UB': (0, 2, -2), 'UL': (-2, 2, 0),
                   'UR': (2, 2, 0), 'DF': (0, -2, 2), 'DB': (0, -2, -2),
                   'DL': (-2, -2, 0), 'DR': (2, -2, 0), 'FL': (-2, 0, 2),
                   'FR': (2, 0, 2), 'BL': (-2, 0, -2), 'BR': (2, 0, -2),
                   'UFL': (-2, 2, 2), 'URF': (2, 2, 2),
                   'ULB': (-2, 2, -2), 'UBR': (2, 2, -2),
                   'DLF': (-2, -2, 2), 'DFR': (2, -2, 2),
                   'DBL': (-2, -2, -2), 'DRB': (2, -2, -2)}