'''
Omnidirectional sensor for feature detection
Limited sensor range
Estimate distance and bearing(direction) of observed feature
'''

from map import MapClass
from shapely.geometry import *
import numpy as np
from functions import *
import pygame
from visualization import *

class Sensor(object):
    nr_sensors = 12
    sensor_range =180
    def __init__(self):
        self.sensors_lines = []
        self.sensors_bearing = []
        self.sensors_distance = [None] * 12

    def initilize_sensors(self, bot_c):
        initilizating_sensor_lines = []
        for i in range(self.nr_sensors):
            initilizating_sensor_lines.append(LineString(
                [bot_c, (bot_c.x + self.sensor_range * -np.cos(angle + np.radians((i * 360 / self.nb_sensors))),
                         (bot_c.y + self.sensor_range * np.sin(angle + np.radians((i * 360 / self.nb_sensors)))))]
            )
            )
        return self.sensors_lines = initilizating_sensor_lines


    def draw_sensors(self, win, bot_c):

        for i in range(len(self.sensors_lines)):
            det, dist, inter_pt = sensing(maze, radius, self.ssensors_lines[i], bot_c)
            self.sensors_distance[i] = dist

            if det:
                pygame.draw.line(win, pygame.Color("dardgreen"), (int(bot_c.x), int(bot_c.y)),
                                 (int(inter_pt.x), int(inter_pt.y)), 2)
                txt = creat_cont(str(round(dist, 0)))
                win.blit(txt, (inter_pt.x, inter_pt.y))
