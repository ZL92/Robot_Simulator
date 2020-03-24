'''
Omnidirectional sensor for feature detection
Limited sensor range
Estimate distance and bearing(direction) of observed feature
'''

import maze
from shapely.geometry import *
import numpy as np
from functions import *
import pygame
from visualization import *


########### Class ###########
class Sensor(object):
    nr_sensors = 12
    sensor_range =180

    def __init__(self):
        self.sensors_lines = [None] * 12
        self.sensors_bearing = []
        self.sensors_distance = [None] * 12

    def initilize_sensors(self, bot_c, angle):
        for i in range(self.nr_sensors):
            self.sensors_lines[i] = (LineString(
                [bot_c, (bot_c.x + self.sensor_range * -np.cos(angle + np.radians((i * 360 / self.nr_sensors))),
                         (bot_c.y + self.sensor_range * np.sin(angle + np.radians((i * 360 / self.nr_sensors)))))]
                )
                )


    def draw_sensors(self, win, maze, bot_c, radius, angle):

        for i in range(len(self.sensors_lines)):
            det, dist, inter_pt = sensing(maze, radius, self.sensors_lines[i], self.sensor_range, bot_c)
            self.sensors_distance[i] = dist

            if det:
                pygame.draw.line(win, pygame.Color("darkgreen"), (int(bot_c.x), int(bot_c.y)), (int(inter_pt.x), int(inter_pt.y)), 2)
                txt = create_font(str(round(dist, 0)))
                win.blit(txt, (inter_pt.x, inter_pt.y))
            else:
                pygame.draw.line(win, (255, 0, 0), (int(bot_c.x), int(bot_c.y)),
                                 (bot_c.x + self.sensor_range * -np.cos(angle + np.radians(i * 360 / self.nr_sensors)),
                                  (bot_c.y + self.sensor_range * np.sin(angle + np.radians(i * 360 / self.nr_sensors)))))
                txt = create_font(str(round(dist, 0)))
                win.blit(txt, (bot_c.x + self.sensor_range * -np.cos(angle + np.radians(i * 360 / self.nr_sensors)),
                               (bot_c.y + self.sensor_range * np.sin(angle + np.radians(i * 360 / self.nr_sensors)))))


########### functions ###########

def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def sensing(maze, radius, sensors_line, sensor_range, bot_c):
    detect = False
    dist = sensor_range - radius
    inter_pt = None
    for maze_i in maze:
        for n in range(len(maze_i)-1):
            test = LineString([(int(maze_i[n].x), int(maze_i[n].y)),
                               (int(maze_i[n+1].x), int(maze_i[n+1].y))]).intersection(sensors_line)
            if not (test.is_empty):
                detect = True
                inter_pt = test
                dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
            if detect:
                break
        if detect:
            break


    return detect, dist, inter_pt