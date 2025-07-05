"""
    This program is made for fun, feel free to edit it.

    All the Rubik Cube's move are made according to this site: https://jperm.net/3x3/moves
    Made by Gabro_29

"""

import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import randrange
import threading
from colorama import Fore
from colorama import init as colorama_init
from time import time

colorama_init(autoreset=True)
rubik_cube = list()
solved_cube = list()


def faces(num_faces: str, face: str, translate: list, rotate: list, color_1="white", color_2="blue", color_3="white",
          color_line="black"):
    """Create the face base on color"""

    facesbuff = (
        (1, -1, -1),
        (1, 1, -1),
        (1, 1, 1),
        (1, -1, 1),  # One face stop len 4
        (-1, -1, 1),
        (-1, 1, 1),  # Two faces stop len 6
        (-1, 1, -1)
    )

    facesbordbuff = (
        (0, 1),
        (0, 3),
        (2, 3),
        (2, 1),  # One face stop len 4
        (2, 5),
        (3, 4),
        (5, 4),  # Two faces stop len 7 = 6 +1
        (5, 6),
        (6, 1)  # three faces stop len 10
    )

    insidefaces = (
        (0, 3, 2, 1),
        (2, 3, 4, 5),
        (1, 2, 5, 6)
    )

    numface = {"one": 4, "two": 7, "three": 10, "ONE": 0, "TWO": 1, "THREE": 2}
    numarea = {"one": 4, "two": 6, "three": 7}
    pair_colors = {"white": (1, 1, 1), "blue": (0, 0, 1), "red": (1, 0.2, 0.3), "orange": (1, 0.5, 0.1),
                   "green": (0, 1, 0), "yellow": (1, 1, 0), "black": (0, 0, 0)}

    glTranslated(translate[0], translate[1], translate[2])
    glRotated(rotate[0], rotate[1], rotate[2], rotate[3])

    glBegin(GL_QUADS)
    if face == "ONE":
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
    elif face == "TWO":
        for vertex in insidefaces[numface.get("ONE")]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_2))
            glVertex3fv(facesbuff[vertex])
    elif face == "THREE":
        for vertex in insidefaces[numface.get("ONE")]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
        for vertex in insidefaces[numface.get("TWO")]:
            glColor3fv(pair_colors.get(color_2))
            glVertex3fv(facesbuff[vertex])
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_3))
            glVertex3fv(facesbuff[vertex])
    glEnd()

    glBegin(GL_LINES)
    count = 0
    for line in facesbordbuff:
        if count < numface.get(num_faces):
            for point in line:
                glColor3fv(pair_colors.get(color_line))
                glVertex3fv(facesbuff[point])
            count += 1
        else:
            break
    glEnd()

    # glTranslated(-(translate[0]), -(translate[1]), -(translate[2]))
    glRotated(-rotate[0], (rotate[1]), (rotate[2]), (rotate[3]))


def faces_pos(num_faces: str, face: str, translate: list, rotate: list, color_1="white", color_2="blue",
              color_3="white", color_line="black"):
    """Adjust pos of faces on the screen"""

    faces(num_faces, face, translate, rotate, color_1, color_2, color_3, color_line)
    glTranslated(-translate[0], -translate[1], -translate[2])


def f_layer(layer: list):
    """Create the first layer"""

    faces_pos("three", "THREE", [0, 3, 0], [90, 0, -1, 0], layer[0][0], layer[0][1], layer[0][2])

    faces_pos("two", "TWO", [2, 3, 0], [90, 0, 0, 1], layer[1][0], layer[1][1])

    faces_pos("three", "THREE", [4, 3, 0], [0, 0, 0, 0], layer[2][0], layer[2][1], layer[2][2])

    faces_pos("two", "TWO", [4, 3, -2], [90, -1, 0, 0], layer[3][0], layer[3][1])

    faces_pos("three", "THREE", [4, 3, -4], [90, -1, 0, 0], layer[4][0], layer[4][1], layer[4][2])

    faces_pos("two", "TWO", [2, 3, -4], [180, 1, 1, 0], layer[5][0], layer[5][1])

    faces_pos("three", "THREE", [0, 3, -4], [180, 0, -1, 0], layer[6][0], layer[6][1], layer[6][2])

    faces_pos("two", "TWO", [0, 3, -2], [180, 0, 1, 1], layer[7][0], layer[7][1])

    faces_pos("one", "ONE", [2, 3, -2], [180, 1, 1, 0], layer[8][0])


def s_layer(layer: list):
    """Create the second layer"""

    faces_pos("two", "TWO", [0, 1, 0], [90, 0, -1, 0], layer[0][0], layer[0][1])

    faces_pos("one", "ONE", [2, 1, 2], [90, 0, 1, 0], layer[1][0])

    faces_pos("two", "TWO", [4, 1, 0], [180, 1, 0, 1], layer[2][0], layer[2][1])

    faces_pos("one", "ONE", [4, 1, -2], [0, 0, 0, 0], layer[3][0])

    faces_pos("two", "TWO", [4, 1, -4], [90, 0, 1, 0], layer[4][0], layer[4][1])

    faces_pos("one", "ONE", [2, 1, -4], [90, 0, 1, 0], layer[5][0])

    faces_pos("two", "TWO", [0, 1, -4], [180, 1, 0, -1], layer[6][0], layer[6][1])

    faces_pos("one", "ONE", [-2, 1, -2], [0, 0, 0, 0], layer[7][0])


def t_layer(layer: list):
    """Create the third layer"""

    faces_pos("three", "THREE", [0, -1, 0], [180, 0, 0, 1], layer[0][0], layer[0][1], layer[0][2])

    faces_pos("two", "TWO", [2, -1, 0], [90, 0, 0, -1], layer[1][0], layer[1][1])

    faces_pos("three", "THREE", [4, -1, 0], [90, 0, 0, -1], layer[2][0], layer[2][1], layer[2][2])

    faces_pos("two", "TWO", [4, -1, -2], [90, 1, 0, 0], layer[3][0], layer[3][1])

    faces_pos("three", "THREE", [4, -1, -4], [180, -100, -1, 0], layer[4][0], layer[4][1], layer[4][2])

    faces_pos("two", "TWO", [2, -1, -4], [180, -100, 100, -1], layer[5][0], layer[5][1])

    faces_pos("three", "THREE", [0, -1, -4], [180, -1, 1, 0], layer[6][0], layer[6][1], layer[6][2])

    faces_pos("two", "TWO", [0, -1, -2], [180, 0, -100, 100], layer[7][0], layer[7][1])

    faces_pos("one", "ONE", [2, -3, -2], [90, 0, -1, 100], layer[8][0])


def u_first_animation(m, cube: list):
    """U' animation"""

    if type(m) == list:
        k = 0
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        while k < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            s_layer(cube[9:17])
            t_layer(cube[17:])
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, -2)
            glRotated(k, 0, 1, 0)
            glTranslated(-2, 0, 2)
            f_layer(cube[:9])
            glPopMatrix()
            drawText(50, 120, f"Shuffling cube for {m[2]}/{m[1]} cycles", m[0])
            k += 20
            pygame.display.flip()
    else:
        while m < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            s_layer(cube[9:17])
            t_layer(cube[17:])
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, -2)
            glRotated(m, 0, 1, 0)
            glTranslated(-2, 0, 2)
            f_layer(cube[:9])
            glPopMatrix()
            m += 3
            pygame.display.flip()


def u_animation(m: int, cube: list):
    """U animation"""

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        s_layer(cube[9:17])
        t_layer(cube[17:])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 0, -1, 0)
        glTranslated(-2, 0, 2)
        f_layer(cube[:9])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def r_animation(m: int, cube: list):
    """R animation"""

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        s_layer([cube[9], cube[10], cube[20], cube[12], cube[3], cube[14], cube[15], cube[16]])
        t_layer([cube[17], cube[18], cube[21], cube[13], cube[4], cube[22], cube[23], cube[24], cube[25]])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 1, 0, 0)
        f_layer([cube[0], cube[1], cube[19], cube[11], cube[2], cube[5], cube[6], cube[7], cube[8]])
        glTranslated(-2, 0, 2)
        glPopMatrix()
        m += 3
        pygame.display.flip()


def m_animation(m: int, cube: list):
    """M animation"""

    z_animation(m, cube)
    cube = z_move(cube)

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        f_layer(cube[:9])
        t_layer(cube[17:])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 0, -1, 0)
        glTranslated(-2, 0, 2)
        s_layer(cube[9:17])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def m_first_animation(m: int, cube: list):
    """M' animation"""

    z_animation(m, cube)
    cube = z_move(cube)

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        f_layer(cube[:9])
        t_layer(cube[17:])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 0, 1, 0)
        glTranslated(-2, 0, 2)
        s_layer(cube[9:17])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def e_animation(m, cube: list):
    """E animation"""

    if type(m) == list:
        k = 0
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        while k < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            f_layer(cube[:9])
            t_layer(cube[17:])
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, -2)
            glRotated(k, 0, -1, 0)
            glTranslated(-2, 0, 2)
            s_layer(cube[9:17])
            glPopMatrix()
            drawText(50, 120, f"Shuffling cube for {m[2]}/{m[1]} cycles", m[0])
            k += 20
            pygame.display.flip()
    else:
        while m < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            f_layer(cube[:9])
            t_layer(cube[17:])
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, -2)
            glRotated(m, 0, -1, 0)
            glTranslated(-2, 0, 2)
            s_layer(cube[9:17])
            glPopMatrix()
            m += 3
            pygame.display.flip()


def d_animation(m: int, cube: list):
    """D animation"""

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        f_layer(cube[:9])
        s_layer(cube[9:17])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 0, -1, 0)
        glTranslated(-2, 0, 2)
        t_layer(cube[17:])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def x_first_animation(m: int, cube: list):
    """X' animation"""

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Move first layer
        glPushMatrix()
        glTranslated(-2, 0, -2)
        glRotated(m, 1, 0, 0)
        glTranslated(2, 0, 2)
        f_layer(cube[:9])
        s_layer(cube[9:17])
        t_layer(cube[17:])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def z_animation(m, cube: list):
    """Z animation"""

    if type(m) == list:
        k = 0
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        while k < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, 2)
            glRotated(k, 0, 0, -1)
            glTranslated(-2, 0, -2)
            f_layer(cube[:9])
            s_layer(cube[9:17])
            t_layer(cube[17:])
            glPopMatrix()
            drawText(50, 120, f"Shuffling cube for {m[2]}/{m[1]} cycles", m[0])
            k += 20
            pygame.display.flip()
    else:

        while m < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, 2)
            glRotated(m, 0, 0, -1)
            glTranslated(-2, 0, -2)
            f_layer(cube[:9])
            s_layer(cube[9:17])
            t_layer(cube[17:])
            glPopMatrix()
            m += 3
            pygame.display.flip()


def shuffle_animation(cycle: int, m: int, cube: list, font):
    """Shuffle the cube"""

    k = 1
    while k < cycle:
        u_first_animation([font, cycle, k], cube)
        cube = u_first_move(cube)
        z_animation([font, cycle, k], cube)
        cube = z_move(cube)
        if k % 5 == 0:
            e_animation([font, cycle, k], cube)
            cube = e_move(cube)
        k += 1


def sexy_animation(m: int, cube: list):
    """Do the Sexy Move"""

    z_animation(m, cube)
    cube = z_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    u_animation(m, cube)
    cube = u_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    u_animation(m, cube)
    cube = u_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    u_first_animation(m, cube)
    cube = u_first_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    u_first_animation(m, cube)
    cube = u_first_move(cube)


def u_first_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if len(face) == 2 and 0 <= count < 9:
            temp_cube.append([face[1], face[0]])
        elif count == 2:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 4:
            temp_cube.append([face[2], face[0], face[1]])
        else:
            temp_cube.append(face)

        count += 1

    # Change 3 faces
    temp_0 = temp_cube[0]
    temp_cube[0] = temp_cube[6]
    temp_2 = temp_cube[2]
    temp_cube[2] = temp_0
    temp_4 = temp_cube[4]
    temp_cube[4] = temp_2
    temp_cube[6] = temp_4

    # Change 2 faces
    temp_1 = temp_cube[1]
    temp_cube[1] = temp_cube[7]
    temp_3 = temp_cube[3]
    temp_cube[3] = temp_1
    temp_5 = temp_cube[5]
    temp_cube[5] = temp_3
    temp_cube[7] = temp_5

    return temp_cube


def u_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if len(face) == 2 and 0 <= count < 9:
            temp_cube.append([face[1], face[0]])
        elif count == 2:
            temp_cube.append([face[0], face[1], face[2]])
        elif count == 4:
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 6:
            temp_cube.append([face[1], face[2], face[0]])
        else:
            temp_cube.append(face)
        count += 1

    # Change 3 faces
    temp_6 = temp_cube[6]
    temp_cube[6] = temp_cube[0]
    temp_4 = temp_cube[4]
    temp_cube[4] = temp_6
    temp_2 = temp_cube[2]
    temp_cube[2] = temp_4
    temp_cube[0] = temp_2

    # Change 2 faces
    temp_7 = temp_cube[7]
    temp_cube[7] = temp_cube[1]
    temp_5 = temp_cube[5]
    temp_cube[5] = temp_7
    temp_3 = temp_cube[3]
    temp_cube[3] = temp_5
    temp_cube[1] = temp_3

    return temp_cube


def r_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (11, 20, 13, 3):
            temp_cube.append([face[1], face[0]])
        elif count == 19:
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 4:
            temp_cube.append([face[0], face[1], face[2]])
        elif count == 21:
            temp_cube.append([face[1], face[2], face[0]])
        else:
            temp_cube.append(face)

        count += 1

    # 3 faces
    temp_2 = temp_cube[2]
    temp_cube[2] = temp_cube[19]
    temp_cube[19] = temp_cube[21]
    temp_cube[21] = temp_cube[4]
    temp_cube[4] = temp_2

    # 2 faces
    temp_3 = temp_cube[3]
    temp_cube[3] = temp_cube[11]
    temp_cube[11] = temp_cube[20]
    temp_cube[20] = temp_cube[13]
    temp_cube[13] = temp_3

    return temp_cube


def m_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (1, 5, 18, 22):
            temp_cube.append([face[1], face[0]])
        else:
            temp_cube.append(face)
        count += 1

    temp_1 = temp_cube[1]
    temp_cube[1] = temp_cube[5]
    temp_8 = temp_cube[8]
    temp_cube[8] = temp_cube[14]
    temp_cube[5] = temp_cube[22]
    temp_cube[14] = temp_cube[25]
    temp_cube[22] = temp_cube[18]
    temp_cube[25] = temp_cube[10]
    temp_cube[18] = temp_1
    temp_cube[10] = temp_8

    temp_cube = z_move(temp_cube)

    return temp_cube


def m_first_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (1, 5, 18, 22):
            temp_cube.append([face[1], face[0]])
        else:
            temp_cube.append(face)
        count += 1

    # Change central faces
    temp_5 = temp_cube[5]
    temp_cube[5] = temp_cube[1]
    temp_14 = temp_cube[14]
    temp_cube[14] = temp_cube[8]
    temp_22 = temp_cube[22]
    temp_cube[22] = temp_5
    temp_25 = temp_cube[25]
    temp_cube[25] = temp_14
    temp_18 = temp_cube[18]
    temp_cube[18] = temp_22
    temp_10 = temp_cube[10]
    temp_cube[10] = temp_25
    temp_cube[1] = temp_18
    temp_cube[8] = temp_10

    temp_cube = z_move(temp_cube)

    return temp_cube


def e_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (9, 11, 13, 15):
            temp_cube.append([face[1], face[0]])
        else:
            temp_cube.append(face)
        count += 1

    # Change central faces
    temp_9 = temp_cube[9]
    temp_cube[9] = temp_cube[11]
    temp_10 = temp_cube[10]
    temp_cube[10] = temp_cube[12]
    temp_11 = temp_cube[11]
    temp_cube[11] = temp_cube[13]

    temp_cube[12] = temp_cube[14]
    temp_cube[13] = temp_cube[15]
    temp_cube[14] = temp_cube[16]
    temp_cube[15] = temp_9
    temp_cube[16] = temp_10

    return temp_cube


def d_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (18, 20, 22, 24):
            temp_cube.append([face[1], face[0]])
        elif count == 19:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 21:
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 23:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 17:
            temp_cube.append([face[2], face[0], face[1]])
        else:
            temp_cube.append(face)
        count += 1

    # Change central faces
    temp_17 = temp_cube[17]
    temp_cube[17] = temp_cube[19]
    temp_cube[19] = temp_cube[21]
    temp_cube[21] = temp_cube[23]
    temp_cube[23] = temp_17

    temp_18 = temp_cube[18]
    temp_cube[18] = temp_cube[20]
    temp_cube[20] = temp_cube[22]
    temp_cube[22] = temp_cube[24]
    temp_cube[24] = temp_18

    return temp_cube


def x_first_move(cube: list):
    """Take the cube and rotate it, so place on top the face to move"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if len(face) == 2:
            temp_cube.append([face[1], face[0]])
        elif count in (0, 17, 2):
            temp_cube.append([face[1], face[2], face[0]])
        elif count in (6, 23, 19):
            temp_cube.append([face[2], face[0], face[1]])
        else:
            temp_cube.append(face)
        count += 1

    # Central line
    temp_10 = temp_cube[10]
    temp_cube[10] = temp_cube[8]
    temp_cube[8] = temp_cube[14]
    temp_cube[14] = temp_cube[25]
    temp_cube[25] = temp_10

    temp_18 = temp_cube[18]
    temp_cube[18] = temp_cube[1]
    temp_cube[1] = temp_cube[5]
    temp_cube[5] = temp_cube[22]
    temp_cube[22] = temp_18

    # Edge
    temp_19 = temp_cube[19]
    temp_cube[19] = temp_cube[2]
    temp_cube[2] = temp_cube[4]
    temp_cube[4] = temp_cube[21]
    temp_cube[21] = temp_19

    temp_11 = temp_cube[11]
    temp_cube[11] = temp_cube[3]
    temp_cube[3] = temp_cube[13]
    temp_cube[13] = temp_cube[20]
    temp_cube[20] = temp_11

    temp_17 = temp_cube[17]
    temp_cube[17] = temp_cube[0]
    temp_cube[0] = temp_cube[6]
    temp_cube[6] = temp_cube[23]
    temp_cube[23] = temp_17

    temp_9 = temp_cube[9]
    temp_cube[9] = temp_cube[7]
    temp_cube[7] = temp_cube[15]
    temp_cube[15] = temp_cube[24]
    temp_cube[24] = temp_9

    return temp_cube


def z_move(cube: list):
    """Take the cube and rotate it, so place on top the face to move"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if len(face) == 2:
            temp_cube.append([face[1], face[0]])
        elif count == 17:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 0:
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 4:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 6:
            temp_cube.append([face[2], face[0], face[1]])
        else:
            temp_cube.append(face)
        count += 1

    # Central Single
    temp_12 = temp_cube[12]
    temp_cube[12] = temp_cube[8]
    temp_cube[8] = temp_cube[16]
    temp_cube[16] = temp_cube[25]
    temp_cube[25] = temp_12

    # Central edges
    temp_20 = temp_cube[20]
    temp_cube[20] = temp_cube[3]
    temp_cube[3] = temp_cube[7]
    temp_cube[7] = temp_cube[24]
    temp_cube[24] = temp_20

    # Right edges

    temp_21 = temp_cube[21]
    temp_cube[21] = temp_cube[4]
    temp_cube[4] = temp_cube[6]
    temp_cube[6] = temp_cube[23]
    temp_cube[23] = temp_21

    # Right central

    temp_13 = temp_cube[13]
    temp_cube[13] = temp_cube[5]
    temp_cube[5] = temp_cube[15]
    temp_cube[15] = temp_cube[22]
    temp_cube[22] = temp_13

    # Left edges

    temp_19 = temp_cube[19]
    temp_cube[19] = temp_cube[2]
    temp_cube[2] = temp_cube[0]
    temp_cube[0] = temp_cube[17]
    temp_cube[17] = temp_19

    # Left central

    temp_11 = temp_cube[11]
    temp_cube[11] = temp_cube[1]
    temp_cube[1] = temp_cube[9]
    temp_cube[9] = temp_cube[18]
    temp_cube[18] = temp_11

    return temp_cube


def sexy_move(cube: list):
    """Do sexy move"""

    cube = z_move(cube)
    cube = z_move(cube)
    cube = z_move(cube)
    cube = u_move(cube)
    cube = z_move(cube)
    cube = u_move(cube)
    cube = z_move(cube)
    cube = z_move(cube)
    cube = z_move(cube)
    cube = u_first_move(cube)
    cube = z_move(cube)
    cube = u_first_move(cube)

    return cube


def drawText(x: int, y: int, text: str, font):
    """Print on the screen how many times is shuffling the cube"""

    textSurface = font.render(text, True, (255, 255, 66, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def shuffle(cycle, cube: list):
    """Take the cube and move the faces to messy the all cube"""

    k = 1
    while k < cycle:
        cube = u_first_move(cube)
        cube = z_move(cube)
        if k % 5 == 0:
            cube = e_move(cube)
        k += 1

    return cube


# Average execution time 6.58 over 100 cycles after shluffle every time
def first_white(cube: list):
    """Try to solve the Cube via Layer Algorithm"""

    print(
        "Start to place the White face on top\nThen find the Orange+White element and move it\nto the correct position")

    # Move white face on the top
    for index in range(len(cube)):
        if cube[index] == ["white"]:
            if index == 14:
                x_first_animation(1, cube)
                cube = x_first_move(cube)
            elif index == 10:
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
            elif index == 16:
                z_animation(1, cube)
                cube = z_move(cube)
            elif index == 25:
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
            elif index == 12:
                z_animation(1, cube)
                cube = z_move(cube)
                z_animation(1, cube)
                cube = z_move(cube)
                z_animation(1, cube)
                cube = z_move(cube)

    # Start to build The White Cross
    start = time()
    try:
        orange_ind = cube.index(["white", "orange"])
    except ValueError:
        orange_ind = 2

    z_done = 0
    x_first_done = 0

    while True:

        # Make some choice on the move to do
        while True:
            a = random.randrange(6)
            if a == 3 and z_done == 4:
                continue
            elif a == 4 and x_first_done == 4:
                continue
            else:
                break

        if a == 0:  # M
            m_animation(1, cube)
            cube = m_move(cube)
            z_done = 0
            x_first_done = 0
        elif a == 1:  # U'
            u_animation(1, cube)
            cube = u_move(cube)
            z_done = 0
            x_first_done = 0
        elif a == 2:  # M'
            m_first_animation(1, cube)
            cube = m_first_move(cube)
            z_done = 0
            x_first_done = 0
        elif a == 3:  # Z
            z_animation(1, cube)
            cube = z_move(cube)
            z_done += 1
        elif a == 4:  # X'
            x_first_animation(1, cube)
            cube = x_first_move(cube)
            x_first_done += 1
        elif a == 5:
            sexy_animation(1, cube)
            cube = sexy_move(cube)
            z_done = 0
            x_first_done = 0

        # Make again white element on top
        for index in range(len(cube)):
            if cube[index] == ["white"]:
                if index == 14:
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                elif index == 10:
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                elif index == 16:
                    z_animation(1, cube)
                    cube = z_move(cube)
                elif index == 25:
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                elif index == 12:
                    z_animation(1, cube)
                    cube = z_move(cube)
                    z_animation(1, cube)
                    cube = z_move(cube)
                    z_animation(1, cube)
                    cube = z_move(cube)

        try:
            orange_ind = cube.index(["white", "orange"])
        except ValueError:
            orange_ind = cube.index(["orange", "white"])

        try:
            if orange_ind == 1 and cube[orange_ind] == ["white", "orange"]:
                break
        except ValueError:
            pass

    end = time()
    print(
        "White element and Orange+White element placed in" + Fore.RED + f" {round(end - start, 2)} " + Fore.RESET + "seconds.....Move on next")

    return cube


def white_cross(cube: list):
    """Make white cross after made first_white function"""

    # Get the indexs
    def get_index(cube: list):
        try:
            green_ind = cube.index(["green", "white"])
        except ValueError:
            green_ind = cube.index(["white", "green"])

        try:
            red_ind = cube.index(["white", "red"])
        except ValueError:
            red_ind = cube.index(["red", "white"])

        try:
            blue_ind = cube.index(["blue", "white"])
        except ValueError:
            blue_ind = cube.index(["white", "blue"])

        return green_ind, red_ind, blue_ind

    # Possible moves to do whitout touch white and orange
    def right_move(cube: list):
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)

        return cube

    def left_move(cube: list):
        z_animation(1, cube)
        cube = z_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)

        return cube

    green_ind, red_ind, blue_ind = get_index(cube)

    # Try right moves to get one piece of the cross
    k = 0
    element_in_3_pos = ""
    element_in_7_pos = ""

    print(
        "Lets find out the next element:\n-" + Fore.GREEN + "Green" + Fore.RESET + "+White\n-" + Fore.BLUE + "Blue" + Fore.RESET + "+White" + "\n-" + Fore.RED + "Red" + Fore.RESET + "+White")

    while cube[3] != ["green", "white"] and cube[7] != ["blue", "white"] and cube[5] != ["white", "red"]:
        k = 0
        element_in_3_pos = ""
        element_in_7_pos = ""

        while k < 4:
            cube = right_move(cube)
            green_ind, red_ind, blue_ind = get_index(cube)
            if green_ind == 3 or red_ind == 3 or blue_ind == 3:
                if green_ind == 3:
                    element_in_3_pos = "green"
                elif red_ind == 3:
                    element_in_3_pos = "red"
                else:
                    element_in_3_pos = "blue"
                break
            else:
                element_in_3_pos = "none"
                k += 1

        # Move found element in the correct position base on the color
        if element_in_3_pos == "green":
            if cube[green_ind] == ["green", "white"]:
                pass
            else:
                cube = right_move(cube)
                e_animation(1, cube)
                cube = e_move(cube)
                cube = right_move(cube)
        elif element_in_3_pos == "red":
            if cube[red_ind] == ["red", "white"]:
                cube = right_move(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                cube = right_move(cube)
                cube = right_move(cube)
                cube = right_move(cube)
                u_first_animation(1, cube)
                cube = u_first_move(cube)
            else:
                cube = right_move(cube)
                e_animation(1, cube)
                cube = e_move(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                cube = right_move(cube)
                u_first_animation(1, cube)
                cube = u_first_move(cube)
        elif element_in_3_pos == "blue":
            if cube[blue_ind] == ["white", "blue"]:
                cube = right_move(cube)
                e_animation(1, cube)
                cube = e_move(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                cube = right_move(cube)
                u_first_animation(1, cube)
                cube = u_first_move(cube)
                u_first_animation(1, cube)
                cube = u_first_move(cube)
            else:
                cube = right_move(cube)
                u_first_animation(1, cube)
                cube = u_first_move(cube)
                u_first_animation(1, cube)
                cube = u_first_move(cube)
                cube = right_move(cube)
                cube = right_move(cube)
                cube = right_move(cube)
                cube = u_first_move(cube)
                u_first_animation(1, cube)
                cube = u_first_move(cube)
                u_first_animation(1, cube)
        elif element_in_3_pos == "none":
            k = 0
            while k < 4:
                cube = left_move(cube)
                green_ind, red_ind, blue_ind = get_index(cube)
                if green_ind == 7 or red_ind == 7 or blue_ind == 7:
                    if green_ind == 7:
                        element_in_7_pos = "green"
                    elif red_ind == 7:
                        element_in_7_pos = "red"
                    else:
                        element_in_7_pos = "blue"
                    break
                else:
                    element_in_7_pos = "none"
                    k += 1

            if element_in_7_pos == "green":
                if cube[green_ind] == ["green", "white"]:
                    cube = left_move(cube)
                    e_animation(1, cube)
                    cube = e_move(cube)
                    e_animation(1, cube)
                    cube = e_move(cube)
                    cube = right_move(cube)
                else:
                    cube = left_move(cube)
                    e_animation(1, cube)
                    cube = e_move(cube)
                    cube = right_move(cube)
                    cube = right_move(cube)
                    cube = right_move(cube)
            elif element_in_7_pos == "red":
                if cube[red_ind] == ["red", "white"]:
                    cube = left_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    cube = left_move(cube)
                    cube = left_move(cube)
                    cube = left_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                else:
                    cube = left_move(cube)
                    e_animation(1, cube)
                    cube = e_move(cube)
                    e_animation(1, cube)
                    cube = e_move(cube)
                    e_animation(1, cube)
                    cube = e_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    cube = left_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
            elif element_in_7_pos == "blue":
                if cube[blue_ind] == ["blue", "white"]:
                    pass
                else:
                    cube = left_move(cube)
                    e_animation(1, cube)
                    cube = e_move(cube)
                    e_animation(1, cube)
                    cube = e_move(cube)
                    e_animation(1, cube)
                    cube = e_move(cube)
                    cube = left_move(cube)
            else:
                d_animation(1, cube)
                cube = d_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)

        if cube[1] == ["white", "orange"]:
            print("Orange its OK")
        if cube[3] == ["green", "white"]:
            print("Green its OK")
        if cube[5] == ["white", "red"]:
            print("Red its OK")
        if cube[7] == ["blue", "white"]:
            print("Blue its OK")

    # Now I have 3 white element on the first layer
    # Look for the third white element by doing left move
    green_ind, red_ind, blue_ind = get_index(cube)

    if green_ind == 3:
        print("I have found the Green+White element")
    elif red_ind == 5:
        print("I have found the Red+White element")
    elif blue_ind == 7:
        print("I have found the Blue+White element")

    if green_ind == 3:
        print("So move on to find the Blue+White or the Red+White element")
        while cube[7] != ["blue", "white"] and cube[5] != ["white", "red"]:
            k = 0
            element_in_7_pos = ""

            while k < 4:
                cube = left_move(cube)
                green_ind, red_ind, blue_ind = get_index(cube)
                if red_ind == 7 or blue_ind == 7:
                    if red_ind == 7:
                        element_in_7_pos = "red"
                    else:
                        element_in_7_pos = "blue"
                    break
                else:
                    element_in_7_pos = "none"
                    k += 1

            if element_in_7_pos == "red":
                if cube[red_ind] == ["red", "white"]:
                    # print("Ho trovato il rosso", cube[red_ind])
                    cube = left_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    cube = left_move(cube)
                    cube = left_move(cube)
                    cube = left_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                else:
                    # print("Ho trovato il rosso", cube[red_ind])
                    cube = left_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
            elif element_in_7_pos == "blue":
                if cube[blue_ind] == ["blue", "white"]:
                    pass
                else:
                    # print("Ho trovato il blu", cube[blue_ind])
                    cube = left_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
            elif element_in_7_pos == "none":
                d_animation(1, cube)
                cube = d_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)

        if cube[1] == ["white", "orange"]:
            print("Orange its OK")
        if cube[3] == ["green", "white"]:
            print("Green its OK")
        if cube[5] == ["white", "red"]:
            print("Red its OK")
        if cube[7] == ["blue", "white"]:
            print("Blue its OK")

    elif blue_ind == 7:
        print("So move on to find the Green+White or the Red+White element")
        while cube[3] != ["green", "white"] and cube[5] != ["white", "red"]:
            k = 0
            element_in_3_pos = ""
            while k < 4:
                cube = right_move(cube)
                green_ind, red_ind, blue_ind = get_index(cube)
                if green_ind == 3 or red_ind == 3:
                    if green_ind == 3:
                        element_in_3_pos = "green"
                    elif red_ind == 3:
                        element_in_3_pos = "red"
                    break
                else:
                    element_in_3_pos = "none"
                    k += 1

            # Move found element in the correct position base on the color
            if element_in_3_pos == "green":
                if cube[green_ind] == ["green", "white"]:
                    pass
                else:
                    # print("Ho trovato il verde", cube[green_ind])
                    cube = right_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
            elif element_in_3_pos == "red":
                if cube[red_ind] == ["red", "white"]:
                    # print("Ho trovato il rosso", cube[red_ind])
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                else:
                    # print("Ho trovato il rosso", cube[red_ind])
                    cube = right_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
            elif element_in_3_pos == "none":
                d_animation(1, cube)
                cube = d_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)
                x_first_animation(1, cube)
                cube = x_first_move(cube)

        if cube[1] == ["white", "orange"]:
            print("Orange its OK")
        if cube[3] == ["green", "white"]:
            print("Green its OK")
        if cube[5] == ["white", "red"]:
            print("Red its OK")
        if cube[7] == ["blue", "white"]:
            print("Blue its OK")

    else:  # RED
        print("So move on to find the Green+White or the Blue+White element")
        while cube[3] != ["green", "white"] and cube[7] != ["blue", "white"]:
            k = 0
            element_in_3_pos = ""
            element_in_7_pos = ""

            while k < 4:
                cube = right_move(cube)
                green_ind, red_ind, blue_ind = get_index(cube)
                if green_ind == 3 or blue_ind == 3:
                    if green_ind == 3:
                        element_in_3_pos = "green"
                    else:
                        element_in_3_pos = "blue"
                    break
                else:
                    element_in_3_pos = "none"
                    k += 1

            # Move found element in the correct position base on the color
            if element_in_3_pos == "green":
                if cube[green_ind] == ["green", "white"]:
                    pass
                else:
                    # print("Ho trovato il verde", cube[green_ind])
                    cube = right_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
            elif element_in_3_pos == "blue":
                if cube[blue_ind] == ["white", "blue"]:
                    # print("Ho trovato il blu", cube[blue_ind])
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    z_animation(1, cube)
                    cube = z_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                else:
                    # print("Ho trovato il blu", cube[blue_ind])
                    cube = right_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    cube = right_move(cube)
                    cube = right_move(cube)
                    cube = right_move(cube)
                    cube = u_first_move(cube)
                    u_first_animation(1, cube)
                    cube = u_first_move(cube)
                    u_first_animation(1, cube)
            elif element_in_3_pos == "none":
                k = 0
                while k < 4:
                    cube = left_move(cube)
                    green_ind, red_ind, blue_ind = get_index(cube)
                    if green_ind == 7 or blue_ind == 7:
                        if green_ind == 7:
                            element_in_7_pos = "green"
                        else:
                            element_in_7_pos = "blue"
                        break
                    else:
                        element_in_7_pos = "none"
                        k += 1

                if element_in_7_pos == "green":
                    if cube[green_ind] == ["green", "white"]:
                        # print("Ho trovato il verde", cube[green_ind])
                        cube = left_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        cube = right_move(cube)
                        cube = right_move(cube)
                        cube = right_move(cube)
                    else:
                        # print("Ho trovato il verde", cube[green_ind])
                        cube = left_move(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        u_animation(1, cube)
                        cube = u_move(cube)
                elif element_in_7_pos == "blue":
                    if cube[blue_ind] == ["blue", "white"]:
                        pass
                    else:
                        # print("Ho trovato il blu", cube[blue_ind])
                        cube = left_move(cube)
                        u_animation(1, cube)
                        cube = u_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        x_first_animation(1, cube)
                        cube = x_first_move(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                else:
                    d_animation(1, cube)
                    cube = d_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    u_animation(1, cube)
                    cube = u_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)
                    x_first_animation(1, cube)
                    cube = x_first_move(cube)

        if cube[1] == ["white", "orange"]:
            print("Orange its OK")
        if cube[3] == ["green", "white"]:
            print("Green its OK")
        if cube[5] == ["white", "red"]:
            print("Red its OK")
        if cube[7] == ["blue", "white"]:
            print("Blue its OK")

    # Now I have three white element on the first layer
    # Lets find out the fourth one

    green_ind, red_ind, blue_ind = get_index(cube)

    if green_ind == 3 and red_ind == 5:
        print("I have found Green+White and Red+White...Lets find out the Blue+White")
    elif blue_ind == 7 and red_ind == 5:
        print("I have found Blue+White and Red+White...Lets find out the Green+White")
    elif blue_ind == 7 and green_ind == 3:
        print("I have found Green+White and Blue+White...Lets find out the Red+White")

    if green_ind == 3 and red_ind == 5:
        while cube[7] != ["blue", "white"]:
            green_ind, red_ind, blue_ind = get_index(cube)
            if blue_ind in (15, 24, 9):
                cube = left_move(cube)
            elif blue_ind in (11, 13):
                e_animation(1, cube)
                cube = e_move(cube)
            elif blue_ind in (18, 20, 22):
                d_animation(1, cube)
                cube = d_move(cube)
            elif cube[7] == ["white", "blue"]:
                cube = left_move(cube)
                e_animation(1, cube)
                cube = e_move(cube)
                e_animation(1, cube)
                cube = e_move(cube)
                e_animation(1, cube)
                cube = e_move(cube)
                cube = left_move(cube)

        if cube[1] == ["white", "orange"]:
            print("Orange its OK")
        if cube[3] == ["green", "white"]:
            print("Green its OK")
        if cube[5] == ["white", "red"]:
            print("Red its OK")
        if cube[7] == ["blue", "white"]:
            print("Blue its OK")

    elif blue_ind == 7 and red_ind == 5:
        while cube[3] != ["green", "white"]:
            green_ind, red_ind, blue_ind = get_index(cube)
            if green_ind in (13, 20, 11):
                cube = right_move(cube)
            elif green_ind in (9, 15):
                e_animation(1, cube)
                cube = e_move(cube)
            elif green_ind in (18, 24, 22):
                d_animation(1, cube)
                cube = d_move(cube)
            elif cube[3] == ["white", "green"]:
                cube = right_move(cube)
                e_animation(1, cube)
                cube = e_move(cube)
                cube = right_move(cube)

        if cube[1] == ["white", "orange"]:
            print("Orange its OK")
        if cube[3] == ["green", "white"]:
            print("Green its OK")
        if cube[5] == ["white", "red"]:
            print("Red its OK")
        if cube[7] == ["blue", "white"]:
            print("Blue its OK")

    elif blue_ind == 7 and green_ind == 3:
        while cube[5] != ["white", "red"]:
            u_animation(1, cube)
            cube = u_move(cube)
            green_ind, red_ind, blue_ind = get_index(cube)
            if red_ind in (13, 20, 11):
                cube = right_move(cube)
            elif red_ind in (9, 15):
                e_animation(1, cube)
                cube = e_move(cube)
            elif red_ind in (18, 24, 22):
                d_animation(1, cube)
                cube = d_move(cube)
            elif cube[3] == ["white", "red"]:
                cube = right_move(cube)
                e_animation(1, cube)
                cube = e_move(cube)
                cube = right_move(cube)

            u_first_animation(1, cube)
            cube = u_first_move(cube)

        if cube[1] == ["white", "orange"]:
            print("Orange its OK")
        if cube[3] == ["green", "white"]:
            print("Green its OK")
        if cube[5] == ["white", "red"]:
            print("Red its OK")
        if cube[7] == ["blue", "white"]:
            print("Blue its OK")

    print("""White cross completed...\nNow I align the color by moving the second layer""")

    while cube[10] != ["orange"]:
        e_animation(1, cube)
        cube = e_move(cube)

    if cube[1] == ["white", "orange"] and cube[3] == ["green", "white"] and cube[5] == ["white", "red"] \
            and cube[7] == ["blue", "white"]:
        print("White Cross Check OK")
    else:
        print("There is some problem with the cross")

    print("""White cross completed and single element color aligned""")

    return cube


def white_face(cube: list):
    """Complete the White face"""

    def right_move(cube: list):
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)

        return cube

    def left_move(cube: list):
        z_animation(1, cube)
        cube = z_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)

        return cube

    print("Start to solve White face....First place it on the bottom")

    # Put white face on the bottom
    z_animation(1, cube)
    cube = z_move(cube)
    z_animation(1, cube)
    cube = z_move(cube)

    # Let's find the White+Orange+Blue element
    WOB_index = 0
    for index in range(len(cube)):
        if "white" in cube[index] and "orange" in cube[index] and "blue" in cube[index]:
            WOB_index = index
            print(f"White+Orange+Blue element found in position {WOB_index}")

    # Put the found element in the correct position
    while cube[19] != ["white", "orange", "blue"]:
        if WOB_index in (2, 19):
            sexy_animation(1, cube)
            cube = sexy_move(cube)
        elif WOB_index in (0, 6, 4):
            u_first_animation(1, cube)
            cube = u_first_move(cube)
        elif WOB_index == 17:
            cube = left_move(cube)
            u_first_animation(1, cube)
            cube = u_first_move(cube)
            cube = left_move(cube)
            cube = left_move(cube)
            cube = left_move(cube)
        elif WOB_index == 23:
            d_animation(1, cube)
            cube = d_move(cube)
            d_animation(1, cube)
            cube = d_move(cube)
            sexy_animation(1, cube)
            cube = sexy_move(cube)
            d_animation(1, cube)
            cube = d_move(cube)
            d_animation(1, cube)
            cube = d_move(cube)
        elif WOB_index == 21:
            d_animation(1, cube)
            cube = d_move(cube)
            sexy_animation(1, cube)
            cube = sexy_move(cube)
            d_animation(1, cube)
            cube = d_move(cube)
            d_animation(1, cube)
            cube = d_move(cube)
            d_animation(1, cube)
            cube = d_move(cube)

        for index in range(len(cube)):
            if "white" in cube[index] and "orange" in cube[index] and "blue" in cube[index]:
                WOB_index = index

    # Let's find the White+Orange+Green element
    WOG_index = 0
    for index in range(len(cube)):
        if "white" in cube[index] and "orange" in cube[index] and "green" in cube[index]:
            WOG_index = index
            print(f"White+Orange+Green element found in position {WOG_index}")

    # Put the found element in the correct position
    while cube[17] != ['green', 'orange', 'white']:
        d_animation(1, cube)
        cube = d_move(cube)
        d_animation(1, cube)
        cube = d_move(cube)
        d_animation(1, cube)
        cube = d_move(cube)

        for index in range(len(cube)):
            if "white" in cube[index] and "orange" in cube[index] and "green" in cube[index]:
                WOG_index = index

        if WOG_index in (2, 19):
            sexy_animation(1, cube)
            cube = sexy_move(cube)
        elif WOG_index in (0, 6, 4):
            u_first_animation(1, cube)
            cube = u_first_move(cube)
        elif WOG_index == 17:
            cube = left_move(cube)
            u_first_animation(1, cube)
            cube = u_first_move(cube)
            cube = left_move(cube)
            cube = left_move(cube)
            cube = left_move(cube)
        elif WOG_index == 23:
            z_animation(1, cube)
            cube = z_move(cube)
            u_first_animation(1, cube)
            cube = u_first_move(cube)
            u_first_animation(1, cube)
            cube = u_first_move(cube)
            sexy_animation(1, cube)
            cube = sexy_move(cube)
            u_first_animation(1, cube)
            cube = u_first_move(cube)
            z_animation(1, cube)
            cube = z_move(cube)
            z_animation(1, cube)
            cube = z_move(cube)
            z_animation(1, cube)
            cube = z_move(cube)

        d_animation(1, cube)
        cube = d_move(cube)

    # Let's find the White+Green+Red element
    WGR_index = 0
    for index in range(len(cube)):
        if "white" in cube[index] and "green" in cube[index] and "red" in cube[index]:
            WGR_index = index
            print(f"White+Green+Red element found in position {WGR_index}")

    # Put the found element in the correct position
    while cube[23] != ['white', 'red', 'green']:
        d_animation(1, cube)
        cube = d_move(cube)
        d_animation(1, cube)
        cube = d_move(cube)

        for index in range(len(cube)):
            if "white" in cube[index] and "green" in cube[index] and "red" in cube[index]:
                WGR_index = index

        if WGR_index in (2, 19):
            sexy_animation(1, cube)
            cube = sexy_move(cube)
        elif WGR_index in (0, 6, 4):
            u_first_animation(1, cube)
            cube = u_first_move(cube)
        elif WGR_index == 17:
            cube = left_move(cube)
            u_first_animation(1, cube)
            cube = u_first_move(cube)
            cube = left_move(cube)
            cube = left_move(cube)
            cube = left_move(cube)

        d_animation(1, cube)
        cube = d_move(cube)
        d_animation(1, cube)
        cube = d_move(cube)

    # Let's find the White+Red+Blue element
    WRB_index = 0
    for index in range(len(cube)):
        if "white" in cube[index] and "blue" in cube[index] and "red" in cube[index]:
            WRB_index = index
            print(f"White+Red+Blue element found in position {WRB_index}")

    # Put the found element in the correct position
    while cube[21] != ['blue', 'red', 'white']:
        d_animation(1, cube)
        cube = d_move(cube)

        for index in range(len(cube)):
            if "white" in cube[index] and "blue" in cube[index] and "red" in cube[index]:
                WRB_index = index

        if WRB_index in (2, 19):
            sexy_animation(1, cube)
            cube = sexy_move(cube)
        elif WRB_index in (0, 6, 4):
            u_first_animation(1, cube)
            cube = u_first_move(cube)

        d_animation(1, cube)
        cube = d_move(cube)
        d_animation(1, cube)
        cube = d_move(cube)
        d_animation(1, cube)
        cube = d_move(cube)

    print("White face CHECK completed!")

    return cube


def second_layer(cube: list):
    """Move on second layer"""

    def right_move(cube: list):
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)

        return cube

    def left_move(cube: list):
        z_animation(1, cube)
        cube = z_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)

        return cube

    def move_to_left(cube: list):
        """Move element from top layer to second"""

        u_first_animation(1, cube)
        cube = u_first_move(cube)
        cube = left_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        cube = left_move(cube)
        cube = left_move(cube)
        cube = left_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)

        return cube

    def move_to_right(cube: list):
        """Move element from top layer to second"""

        u_animation(1, cube)
        cube = u_move(cube)
        cube = right_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        cube = right_move(cube)
        cube = right_move(cube)
        cube = right_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)

        return cube

    # Let's find the Orange+Blue element
    OB_index = 0
    for index in range(len(cube)):
        if "orange" in cube[index] and "blue" in cube[index] and len(cube[index]) == 2:
            OB_index = index
            print(f"Orange+Blue element found in position {OB_index}")

    while cube[1] != ["blue", "orange"]:

        if OB_index in (3, 5, 7):
            u_first_animation(1, cube)
            cube = u_first_move(cube)
        elif OB_index == 15:
            e_animation(1, cube)
            cube = e_move(cube)
            e_animation(1, cube)
            cube = e_move(cube)
            e_animation(1, cube)
            cube = e_move(cube)
            cube = move_to_left(cube)
            e_animation(1, cube)
            cube = e_move(cube)
        elif OB_index == 13:
            e_animation(1, cube)
            cube = e_move(cube)
            cube = move_to_right(cube)
            e_animation(1, cube)
            cube = e_move(cube)
            e_animation(1, cube)
            cube = e_move(cube)
            e_animation(1, cube)
            cube = e_move(cube)
        elif OB_index == 11:
            cube = move_to_right(cube)
        elif OB_index == 9:
            cube = move_to_left(cube)
        elif cube[1] == ["orange", "blue"]:
            cube = move_to_left(cube)
            cube = move_to_left(cube)

        for index in range(len(cube)):
            if "orange" in cube[index] and "blue" in cube[index] and len(cube[index]) == 2:
                OB_index = index

    cube = move_to_right(cube)

    # Check position of element after move
    for index in range(len(cube)):
        if "orange" in cube[index] and "blue" in cube[index] and len(cube[index]) == 2:
            OB_index = index
            print(f"Orange+Blue placed in position {OB_index} and it must be in position 11")
            if OB_index != 11:
                print("Error in positioning Orange+Blue element")
                break

    # Let's find the Orange+Blue element
    OG_index = 0
    for index in range(len(cube)):
        if "orange" in cube[index] and "green" in cube[index] and len(cube[index]) == 2:
            OG_index = index
            print(f"Orange+Green element found in position {OG_index}")

    while cube[1] != ["green", "orange"]:

        if OG_index in (3, 5, 7):
            u_first_animation(1, cube)
            cube = u_first_move(cube)
        elif OG_index == 15:
            e_animation(1, cube)
            cube = e_move(cube)
            e_animation(1, cube)
            cube = e_move(cube)
            e_animation(1, cube)
            cube = e_move(cube)
            cube = move_to_left(cube)
            e_animation(1, cube)
            cube = e_move(cube)
        elif OG_index == 13:
            e_animation(1, cube)
            cube = e_move(cube)
            cube = move_to_right(cube)
            e_animation(1, cube)
            cube = e_move(cube)
            e_animation(1, cube)
            cube = e_move(cube)
            e_animation(1, cube)
            cube = e_move(cube)
        elif OG_index == 9:
            cube = move_to_left(cube)
        elif cube[1] == ["orange", "green"]:
            cube = move_to_left(cube)
            cube = move_to_left(cube)

        for index in range(len(cube)):
            if "orange" in cube[index] and "green" in cube[index] and len(cube[index]) == 2:
                OG_index = index

    cube = move_to_left(cube)

    # Check position of element after move
    for index in range(len(cube)):
        if "orange" in cube[index] and "green" in cube[index] and len(cube[index]) == 2:
            OG_index = index
            print(f"Orange+Green placed in position {OG_index} and it must be in position 9")
            if OG_index != 9:
                print("Error in positioning Orange+Green element")
                break

    # Let's find the Red+Blue element
    RB_index = 0
    for index in range(len(cube)):
        if "red" in cube[index] and "blue" in cube[index] and len(cube[index]) == 2:
            RB_index = index
            print(f"Red+Blue element found in position {RB_index}")

    e_animation(1, cube)
    cube = e_move(cube)
    e_animation(1, cube)
    cube = e_move(cube)

    while cube[1] != ["blue", "red"]:

        for index in range(len(cube)):
            if "red" in cube[index] and "blue" in cube[index] and len(cube[index]) == 2:
                RB_index = index

        if RB_index in (3, 5, 7):
            u_first_animation(1, cube)
            cube = u_first_move(cube)
        elif RB_index == 11:
            cube = move_to_right(cube)
        elif RB_index == 20:
            cube = move_to_right(cube)
            cube = move_to_right(cube)
        elif RB_index == 9:
            cube = move_to_left(cube)
        elif cube[1] == ["red", "blue"]:
            cube = move_to_left(cube)
            cube = move_to_left(cube)

    cube = move_to_left(cube)

    # Check position of element after move
    for index in range(len(cube)):
        if "red" in cube[index] and "blue" in cube[index] and len(cube[index]) == 2:
            RB_index = index
            print(f"Red+Blue element placed in position {RB_index} and it must be in position 9")
            if RB_index != 9:
                print("Error in positioning Red+Blue element")
                break

    # Let's find the Red+Green element
    RG_index = 0
    for index in range(len(cube)):
        if "red" in cube[index] and "green" in cube[index] and len(cube[index]) == 2:
            RG_index = index
            print(f"Red+Green element found in position {RG_index}")

    while cube[1] != ["green", "red"]:

        for index in range(len(cube)):
            if "red" in cube[index] and "green" in cube[index] and len(cube[index]) == 2:
                RG_index = index

        if RG_index in (3, 5, 7):
            u_first_animation(1, cube)
            cube = u_first_move(cube)
        elif RG_index == 11:
            cube = move_to_right(cube)
        elif cube[1] == ["red", "green"]:
            cube = move_to_right(cube)
            cube = move_to_right(cube)

    cube = move_to_right(cube)

    # Check position of element after move
    for index in range(len(cube)):
        if "red" in cube[index] and "green" in cube[index] and len(cube[index]) == 2:
            RG_index = index
            print(f"Red+Green element placed in position {RG_index} and it must be in position 11")
            if RG_index != 11:
                print("Error in positioning Red+Green element")
                break

    e_animation(1, cube)
    cube = e_move(cube)
    e_animation(1, cube)
    cube = e_move(cube)

    print("Second layer completed!")

    return cube


def yellow_cross(cube: list):
    """Move on third layer"""

    def l_to_cross(cube: list):
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        cube = sexy_move(cube)
        cube = sexy_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)

        return cube

    def t_to_cross(cube: list):
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        cube = sexy_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        x_first_animation(1, cube)
        cube = x_first_move(cube)

        return cube

    # See if there is an L on the Yellow face
    print("Let's see if there is an L on the top layer")
    k = 0
    L_found = False
    T_found = False
    while True:
        if cube[7][1] == "yellow" and cube[5][0] == "yellow" and cube[3][1] != "yellow":
            L_found = True
            break
        elif "yellow" == cube[7][1] and cube[3][1] == "yellow":
            T_found = True
            break
        elif k == 5:
            break
        u_animation(1, cube)
        cube = u_move(cube)
        k += 1

    if cube[7][1] == "yellow" and cube[5][0] == "yellow" and cube[3][1] == "yellow" and cube[1][0] == "yellow":
        print("Yellow cross already completed")
    elif L_found:  # OK
        print("L found....going to make Yellow Cross")
        cube = l_to_cross(cube)
        print("Yellow cross ompleted")
    elif T_found:  # OK
        print("T found....going to make Yellow Cross")
        cube = t_to_cross(cube)
        print("Yellow cross ompleted")
    else:
        print("Nothing found...going to make Yellow Cross from single element")
        cube = l_to_cross(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        cube = t_to_cross(cube)
        print("Yellow cross ompleted")

    return cube


def adjust_yellow_cross(cube: list):
    """Adjust yellow cross by align color base on second layer"""

    def right_move(cube: list):
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)

        return cube

    def align_4_colors(cube: list):

        cube = right_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        cube = right_move(cube)
        cube = right_move(cube)
        cube = right_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        cube = right_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        cube = right_move(cube)
        cube = right_move(cube)
        cube = right_move(cube)

        return cube

    index_color = {10: "orange", 12: "blue", 14: "red", 16: "green"}

    print("Now I am going to align the colors of the Yellow Cross with the second layer")

    pair = 0
    orange = False
    blue = False
    red = False
    green = False

    # Align Orange, Blue, Green and Red on top layer with second layer colors
    while cube[1][1] != index_color[10] or cube[3][0] != index_color[12] or cube[5][1] != index_color[14] \
            or cube[7][0] != index_color[16]:

        if cube[1] == ["yellow", "orange"] and cube[10] == ["orange"]:
            orange = True
            pair += 1

        if cube[3] == ["blue", "yellow"] and cube[12] == ["blue"]:
            blue = True
            pair += 1

        if cube[5] == ["yellow", "red"] and cube[14] == ["red"]:
            red = True
            pair += 1

        if cube[7] == ["green", "yellow"] and cube[16] == ["green"]:
            green = True
            pair += 1

        if pair >= 2:
            print("Found the two pieces that are paired and going to pair the others")
            u_first_animation(1, cube)
            cube = u_first_move(cube)
            break
        else:
            pair = 0
            orange = False
            blue = False
            red = False
            green = False
            u_animation(1, cube)
            cube = u_move(cube)

    first_count = 0

    for value in [orange, blue, red, green]:
        second_count = 0
        if value:
            for val in [orange, blue, red, green]:
                if val and first_count != second_count:

                    # Orange + Blue
                    if first_count == 0 and second_count == 1:

                        while cube[1] != ["yellow", "orange"]:
                            u_animation(1, cube)
                            cube = u_move(cube)

                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        cube = align_4_colors(cube)
                        u_animation(1, cube)
                        cube = u_move(cube)
                        u_animation(1, cube)
                        cube = u_move(cube)

                        print("Pair found Orange + Blue")

                    # Orange + Red
                    elif first_count == 0 and second_count == 2:

                        while cube[1] != ["yellow", "orange"]:
                            u_animation(1, cube)
                            cube = u_move(cube)

                        cube = align_4_colors(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        cube = align_4_colors(cube)

                        while cube[1] != ["yellow", "orange"]:
                            u_animation(1, cube)
                            cube = u_move(cube)

                        print("Pair found Orange + Red")

                    # Orange + Green
                    elif first_count == 0 and second_count == 3:

                        while cube[1] != ["yellow", "orange"]:
                            u_animation(1, cube)
                            cube = u_move(cube)

                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)

                        cube = align_4_colors(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)

                        print("Pair found Orange + Green")


                    # Blue + Red
                    elif first_count == 1 and second_count == 2:

                        while cube[1] != ["yellow", "blue"]:
                            u_animation(1, cube)
                            cube = u_move(cube)

                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        cube = align_4_colors(cube)
                        u_animation(1, cube)
                        cube = u_move(cube)

                        print("Pair found Blue + Red")


                    # Blue + Green
                    elif first_count == 1 and second_count == 3:

                        while cube[1] != ["yellow", "blue"]:
                            u_animation(1, cube)
                            cube = u_move(cube)

                        cube = align_4_colors(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        cube = align_4_colors(cube)
                        u_animation(1, cube)
                        cube = u_move(cube)

                        print("Pair found Blue + Green")

                    # Red + Green
                    elif first_count == 2 and second_count == 3:

                        while cube[1] != ["yellow", "green"]:
                            u_animation(1, cube)
                            cube = u_move(cube)

                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        u_first_animation(1, cube)
                        cube = u_first_move(cube)
                        cube = align_4_colors(cube)

                        print("Pair found Red + Green")

                second_count += 1

            break
        first_count += 1

    if orange and green and red and blue:
        print("Pieces already paired")

    return cube


def adjust_yellow_face(cube: list):
    """Adjust edge elements"""

    def right_move(cube: list):
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)

        return cube

    def left_move(cube: list):
        z_animation(1, cube)
        cube = z_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)
        z_animation(1, cube)
        cube = z_move(cube)

        return cube

    def right_into_left(cube: list):

        cube = right_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        cube = left_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)
        cube = right_move(cube)
        cube = right_move(cube)
        cube = right_move(cube)
        u_first_animation(1, cube)
        cube = u_first_move(cube)
        cube = left_move(cube)
        cube = left_move(cube)
        cube = left_move(cube)
        u_animation(1, cube)
        cube = u_move(cube)

        return cube

    # Check if other three face elements are OK
    if "orange" in cube[0] and "yellow" in cube[0] and "green" in cube[0] \
            and "blue" in cube[2] and "yellow" in cube[2] and "orange" in cube[2] \
            and "red" in cube[4] and "yellow" in cube[4] and "blue" in cube[4] \
            and "green" in cube[6] and "yellow" in cube[6] and "red" in cube[6]:

        print("All corners in Yellow face are OK....")
        print("Going to put Yellow on the bottom and start to do Sexy Moves")
    else:
        print("Put in the right place the corners")

        while True:

            if "orange" in cube[0] and "yellow" in cube[0] and "green" in cube[0] \
                    and "blue" in cube[2] and "yellow" in cube[2] and "orange" in cube[2] \
                    and "red" in cube[4] and "yellow" in cube[4] and "blue" in cube[4] \
                    and "green" in cube[6] and "yellow" in cube[6] and "red" in cube[6]:
                print("All corners in Yellow face are OK....")
                print("Going to put Yellow on the bottom and start to do Sexy Moves")
                break


            elif "orange" in cube[0] and "yellow" in cube[0] and "green" in cube[0]:

                while cube[1] != ["yellow", "orange"]:
                    u_animation(1, cube)
                    cube = u_move(cube)

                cube = right_into_left(cube)
                print("Orange+Green corner placed")


            elif "green" in cube[6] and "yellow" in cube[6] and "red" in cube[6]:

                while cube[1] != ["yellow", "green"]:
                    u_animation(1, cube)
                    cube = u_move(cube)

                cube = right_into_left(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                print("Green+Red corner placed")


            elif "red" in cube[4] and "yellow" in cube[4] and "blue" in cube[4]:

                while cube[1] != ["yellow", "red"]:
                    u_animation(1, cube)
                    cube = u_move(cube)

                cube = right_into_left(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                u_animation(1, cube)
                cube = u_move(cube)
                print("Red+Blue corner placed")


            elif "blue" in cube[2] and "yellow" in cube[2] and "orange" in cube[2]:

                while cube[1] != ["yellow", "blue"]:
                    u_animation(1, cube)
                    cube = u_move(cube)

                cube = right_into_left(cube)
                u_first_animation(1, cube)
                cube = u_first_move(cube)
                print("Blue+Orange corner placed")


            else:
                cube = right_into_left(cube)
                print("Nothing found so do the move anyway")

    return cube


def final_sexy(cube: list):
    """Put Yellow face on the bottom and do sexy moves"""

    # Put Yellow face on the bottom
    z_animation(1, cube)
    cube = z_move(cube)
    z_animation(1, cube)
    cube = z_move(cube)

    while cube[19] != ["yellow", "orange", "green"]:
        sexy_animation(1, cube)
        cube = sexy_move(cube)

    d_animation(1, cube)
    cube = d_move(cube)

    while cube[19] != ["yellow", "green", "red"]:
        sexy_animation(1, cube)
        cube = sexy_move(cube)

    d_animation(1, cube)
    cube = d_move(cube)

    while cube[19] != ["yellow", "red", "blue"]:
        sexy_animation(1, cube)
        cube = sexy_move(cube)

    d_animation(1, cube)
    cube = d_move(cube)

    while cube[19] != ["yellow", "blue", "orange"]:
        sexy_animation(1, cube)
        cube = sexy_move(cube)

    d_animation(1, cube)
    cube = d_move(cube)

    print("DONE!!!....:)")

    return cube


def solving():
    global rubik_cube

    start = time()
    print("Start to solving the cube")

    if rubik_cube[8] == ["white"] and rubik_cube[1] == ["white", "orange"] \
            and rubik_cube[3] == ["green", "white"] and rubik_cube[5] == ["white", "red"]\
            and rubik_cube[7] == ["blue", "white"]:
        print("White Cross already completed")
    else:
        rubik_cube = first_white(rubik_cube)

        # Save on file Cube disposition
        with open("Rubik Cube.txt", "w") as file:
            file.write("[")
            for line in rubik_cube:
                file.write(f"{line},")
            file.write("]")

        while True:

            if rubik_cube[1] == ["white", "orange"] and rubik_cube[3] == ["green", "white"]\
                    and rubik_cube[5] == ["white", "red"] and rubik_cube[7] == ["blue", "white"]:
                print("White Cross CHECK OK!")
                break
            else:
                rubik_cube = white_cross(rubik_cube)


    rubik_cube = white_face(rubik_cube)

    if rubik_cube[17:] == [["orange", "blue"], ["orange"], ["orange", "green"], ["green"], ["red", "green"], ["red"],
                           ["red", "blue"], ["blue"]]:
        print("Second Layer already completed")
    else:
        rubik_cube = second_layer(rubik_cube)

    if rubik_cube[8] == ["yellow"] and rubik_cube[1] == ["yellow", "orange"] and rubik_cube[3] == ["blue", "yellow"] \
            and rubik_cube[5] == ["yellow", "red"] and rubik_cube[7] == ["green", "yellow"]:
        print("Yellow Cross already completed")
    else:
        rubik_cube = yellow_cross(rubik_cube)

    rubik_cube = adjust_yellow_cross(rubik_cube)
    rubik_cube = adjust_yellow_face(rubik_cube)
    rubik_cube = final_sexy(rubik_cube)

    end = time()

    print(f"Cube solved in {round(end - start, 2)}")


def main():
    """Main code"""

    # Manual definition of layers
    first_layer = [["orange", "blue", "white"], ["white", "orange"], ["green", "orange", "white"],
                   ["green", "white"], ["green", "white", "red"], ["white", "red"], ["blue", "red", "white"],
                   ["blue", "white"], ["white"]]

    second_layer = [["orange", "blue"], ["orange"], ["orange", "green"], ["green"], ["red", "green"],
                    ["red"],
                    ["red", "blue"], ["blue"]]

    third_layer = [["blue", "orange", "yellow"], ["yellow", "orange"], ["yellow", "orange", "green"],
                   ["green", "yellow"], ["green", "red", "yellow"], ["yellow", "red"], ["yellow", "red", "blue"],
                   ["blue", "yellow"], ["yellow"]]

    # Build the cube base on previous layers
    global rubik_cube
    global solved_cube
    for layer in (first_layer, second_layer, third_layer):
        lay = layer
        for face in lay:
            rubik_cube.append(face)

    solved_cube = rubik_cube

    # Initialize pygame gui
    pygame.init()
    pygame.font.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    icon = pygame.image.load('rubik.png')
    pygame.display.set_icon(icon)
    font = pygame.font.SysFont('lucinda console', 64)
    pygame.display.set_caption("Rubik Cube")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(6.0, -1.0, -20)  # Camera view
    glRotatef(45, 1, 1, 1)  # Prospective view

    # No overlapping
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Extra variables
    u_first_key = False
    u_key = False
    r_key = False
    m_key = False
    m_first_key = False
    z_key = False
    x_first_key = False
    shuffle_key = False
    sexy_key = False
    first_white_key = False
    cycle = 0
    m = 1
    prev_pos_x = 0
    prev_pos_y = 0

    # Show the cube on screen
    while True:

        # Check for pressed keys
        for event in pygame.event.get():
            # print(rubik_cube)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:  # Change camera view
                    glRotatef(20, 0, -1, 0)
                if event.key == pygame.K_f:  # Change camera view
                    glRotatef(20, 0, 1, 0)
                # if event.key == pygame.K_s:  # Change camera view
                #     glRotatef(10, 0, 2, 1)
                if event.key == pygame.K_d:  # Change camera view
                    glRotatef(90, 1, 0, 0)
                if event.key == pygame.K_ESCAPE:  # Exit
                    exit()

                # U' Move
                if event.key == pygame.K_o:
                    u_first_animation(m, rubik_cube)
                    u_first_key = True

                # U Move
                if event.key == pygame.K_p:
                    u_animation(m, rubik_cube)
                    u_key = True

                if event.key == pygame.K_r:
                    d_animation(m, rubik_cube)
                    r_key = True

                # M Move
                if event.key == pygame.K_v:
                    m_animation(m, rubik_cube)
                    rubik_cube = m_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    m_key = True

                # M' Move
                if event.key == pygame.K_c:
                    m_first_animation(m, rubik_cube)
                    rubik_cube = m_first_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    m_first_key = True

                # Z Move
                if event.key == pygame.K_t:
                    z_animation(m, rubik_cube)
                    z_key = True

                # X' Move
                if event.key == pygame.K_w:
                    x_first_animation(m, rubik_cube)
                    x_first_key = True

                # Sexy Move
                if event.key == pygame.K_s:
                    sexy_animation(m, rubik_cube)
                    sexy_key = True

                # Shuffle Move
                if event.key == pygame.K_a:
                    cycle = randrange(5, 100)
                    shuffle_animation(cycle, m, rubik_cube, font)
                    shuffle_key = True

                # First White
                if event.key == pygame.K_q:
                    first_white_key = True

        # Mouse Camera
        for event in pygame.mouse.get_pressed(3):
            if event:
                if abs(prev_pos_x - pygame.mouse.get_pos()[0]) == 0:
                    glRotatef(20, 1, 0, 0)  # Camera view
                elif abs(prev_pos_y - pygame.mouse.get_pos()[1]) == 0:
                    glRotatef(20, 0, 1, 0)  # Camera view
                elif abs(prev_pos_y - pygame.mouse.get_pos()[1]) > 1 and abs(
                        prev_pos_x - pygame.mouse.get_pos()[0]) > 1:
                    glRotatef(20, 1, 1, 0)  # Camera view
            prev_pos_x = pygame.mouse.get_pos()[0]
            prev_pos_y = pygame.mouse.get_pos()[1]

        # Clear view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if u_first_key:
            rubik_cube = u_first_move(rubik_cube)
            u_first_key = False
        elif u_key:
            rubik_cube = u_move(rubik_cube)
            u_key = False
        elif r_key:
            rubik_cube = d_move(rubik_cube)
            r_key = False
        elif m_key:
            m_key = False
        elif m_first_key:
            m_first_key = False
        elif x_first_key:
            rubik_cube = x_first_move(rubik_cube)
            x_first_key = False
        elif z_key:
            rubik_cube = z_move(rubik_cube)
            z_key = False
        elif shuffle_key:
            rubik_cube = shuffle(cycle, rubik_cube)
            shuffle_key = False
        elif sexy_key:
            rubik_cube = sexy_move(rubik_cube)
            sexy_key = False
        elif first_white_key:
            threading.Thread(target=solving()).start()
            first_white_key = False

        # Show updated layer
        f_layer(rubik_cube[:9])
        s_layer(rubik_cube[9:17])
        t_layer(rubik_cube[17:])
        pygame.display.flip()
        pygame.time.wait(20)


if __name__ == '__main__':
    main()