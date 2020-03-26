'''
Omnidirectional sensor for feature detection
Limited sensor range
Estimate distance and bearing(direction) of observed feature
'''

#import maze
from shapely.geometry import *
import numpy as np
#from functions import *
import pygame
from visualization import *


########### Class ###########
class Sensor(object):
    nr_sensors = 360
    sensor_range = 100

    def __init__(self):
        self.sensors_lines = [None] * self.nr_sensors
        self.sensors_bearing = []
        self.sensors_distance = [None] * self.nr_sensors

    def initilize_sensors(self, bot_c, angle):
        for i in range(self.nr_sensors):
            self.sensors_lines[i] = (LineString(
                [bot_c, (bot_c.x + self.sensor_range * -np.cos(angle + np.radians((i * 360 / self.nr_sensors))),
                         (bot_c.y + self.sensor_range * np.sin(angle + np.radians((i * 360 / self.nr_sensors)))))]
                )
                )

    def draw_sensors(self, win, beacon_list, bot_c, radius, angle):
        """
        :win: Active window, where to draw
        :beacon_list: List of Points (shapely), of beacons
        :bot_c: Coordinates of center of bot
        :radius: Size / Radius of bot
        :angle: Angle
        """
        
        count_det = 0
        detected_list = []
        dist_list = []
        angle_list = []
        
        for i in range(len(self.sensors_lines)):
            det, dist, inter_pt = sensing_beacons(beacon_list, radius, self.sensors_lines[i], self.sensor_range, bot_c)
            self.sensors_distance[i] = dist
            if det:
                pygame.draw.line(win, (140, 74, 240), (int(bot_c.x), int(bot_c.y)), (int(inter_pt.x), int(inter_pt.y)), 2)
                txt = create_font(str(round(dist, 0)))
                win.blit(txt, (inter_pt.x, inter_pt.y))
                if (inter_pt.x, inter_pt.y) not in detected_list:
                    count_det += 1
                    detected_list.append((inter_pt.x, inter_pt.y))
                    dist_list.append(dist)        
                    print("N sensors: ", len(self.sensors_lines))
                    print("Sensor #{}, angle = {}".format(i, (i*360/len(self.sensors_lines))))
                    angle_list.append((i*360/len(self.sensors_lines)))
            else:
                pass                
        return count_det, detected_list, dist_list, angle_list


########### functions ###########

def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def sensing_beacons(beacon_list, radius, sensors_line, sensor_range, bot_c):
    """
    
    :returns: detect (Bool), dist (int/float), inter_pt (Point)
    """
    detect = False
    inter_pt = None
    dist = None
    
    for beacon in beacon_list[0]:
#        dist = sensor_range - radius
        test = sensors_line.distance(beacon) < 0.8
#        print("test: {}".format(sensors_line.distance(beacon)))
        if test:
            detect = True
            inter_pt = beacon
#            dist = distance(bot_c.coords[0], (beacon.x, beacon.y))
            dist = bot_c.distance(beacon)
            
#    print("Distance : ",dist)
    return detect, dist, inter_pt


def sensing(maze, radius, sensors_line, sensor_range, bot_c):
    # detect = False
    # dist = sensor_range - radius
    detect_list = [False] * len(maze)
    inter_pt_list = np.array([None] * len(maze))
    detected_dist_array = np.array([sensor_range - radius] * len(maze))

    for maze_i in maze:
        dist = sensor_range - radius
        for n in range(len(maze_i)-1):
            test = LineString([(int(maze_i[n].x), int(maze_i[n].y)),
                               (int(maze_i[n+1].x), int(maze_i[n+1].y))]).intersection(sensors_line)
            if not (test.is_empty):
                detect_list[maze.index(maze_i)] = True
                inter_pt_list[maze.index(maze_i)] = test
                dist = np.min([dist, (distance(bot_c.coords[0], test.coords[0]) - radius)])
                break
            # if detect_list[maze.index(maze_i)]:
            #     #One sensor detects only one wall in maze_i.
            #     break
        detected_dist_array[maze.index(maze_i)] = dist

    if any(detect_list): #if anyone is true
        dist = detected_dist_array[np.where(detect_list)[0]].min()
        inter_pt = inter_pt_list[np.where(detect_list)[0]][detected_dist_array[np.where(detect_list)[0]].argmin()]
        # dist = np.min(detected_dist_array[np.nonzero(detected_dist_array)])
        # inter_pt = inter_pt_list[np.argmin(detected_dist_array[np.nonzero(detected_dist_array)])]
        detect = True
    else:
        dist = sensor_range - radius
        inter_pt = None
        detect = False
    return detect, dist, inter_pt
