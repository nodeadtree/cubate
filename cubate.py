# I know this code is an atrocity. I'm just saving it cuz wheee visuals.
import pygame
import random
from pygame.locals import *
from itertools import product
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

def cube(verticies, edges, color):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def the_whole_shebang(vertex_num):
    vertex_list = [np.array([i for i in product([1,-2],[2,-2],[2,-2])])]
    rad = 10000
    rotation_matrix_base = [
            np.array([[1,0,0],
                    [0, cos(1/rad),sin(1/rad)],
                    [0, -sin(1/rad), cos(1/rad)]]),
            np.array([[cos(1/rad), sin(1/rad),0], 
                    [-sin(1/rad), cos(1/rad),0],
                    [0,0,1]]),
            np.array([[ cos(1/rad),0,-sin(1/rad)],
                    [0,1,0], 
                    [sin(1/rad),0, cos(1/rad)]])]
    color = [250,250,250]
    edges = [(0,1),(0,2),(0,4),(1,3),(1,5),(4,5),(2,3),(2,6),(4,6),(5,7),(6,7),(3,7)]
    pygame.init()
    display = (1800,1000)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -10)
    glRotatef(90,0,1,1)

    scale_coefficient = .96
    max_size = 4
    min_size = 1
    frame_count = 0
    rotation_time = 80
    rotation_count = 100
    trail_length = 40
    rotation_matrix = random.choice(rotation_matrix_base)
    modified_rotation_matrix = scale_coefficient * random.choice(rotation_matrix_base)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for verticies in vertex_list:
            cube(verticies, edges, color)
        frame_count = (frame_count + 1) % 6
        rotation_count = (rotation_count + 1) % 60
        if np.linalg.norm(vertex_list[-1][-1]) < min_size:
            random.shuffle(rotation_matrix_base)
            rotation_matrix_base.append(rotation_matrix)
            rotation_matrix = np.matmul(random.choice(rotation_matrix_base), rotation_matrix)
            modified_rotation_matrix = 1 / scale_coefficient * rotation_matrix
        if np.linalg.norm(vertex_list[-1][-1]) > max_size:
            random.shuffle(rotation_matrix_base)
            rotation_matrix = np.matmul(rotation_matrix_base.pop(), rotation_matrix)
            rotation_matrix_base.append(rotation_matrix)
            modified_rotation_matrix = scale_coefficient * rotation_matrix
        vertex_list.append(np.matmul(vertex_list[-1], modified_rotation_matrix))
        vertex_list = vertex_list[-trail_length:]
        pygame.display.flip()
        pygame.time.wait(rotation_time)


the_whole_shebang(8)
