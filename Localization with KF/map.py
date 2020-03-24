'''

Initilizing maze and point-based features
No walls, no collision with features
Known correspondence which means all features have unique labels
screen visualization
'''
import pygame
from visualization import *
from shapely.geometry import *


class MapClass(object):

    map_width = 500
    map_height = 500
    borders = [Point(0, 0), Point(0, map_width), Point(map_height, map_width), Point(map_height, 0)]
    wall1 = [Point(0, 150), Point(350, 150), Point(350, 300), Point (250, 300)]
    wall2 = [Point(150, map_height), Point(150, 250), Point (300, 250)]
    maze = [borders, wall1, wall2]
    features = [Point(0, 0), Point(0, map_width), Point(map_height, map_width), Point(map_height, 0),
                Point(0, 150), Point(350, 150), Point(350, 300), Point (250, 300),
                Point(150, map_height), Point(150, 250), Point (300, 250)]

    def __init__(self):
        self.display_features = True
        self.win = pygame.display.set_mode((self.map_width, self.map_height))

    def initilize_screen(self):
        pygame.display.set_caption('Simulator')
        pygame.init()
        self.win.fill((173, 216, 230))


    def draw_borders(self):
        for i in range(len(self.borders) - 1):
            pygame.draw.line(self.win, (255, 0, 0), (int(self.borders[i].x), int(self.borders[i].y)),
                             (int(self.borders[i + 1].x), int(self.borders[i + 1].y)), 2)
        pygame.draw.line(self.win, (255, 0, 0), (int(self.borders[3].x), int(self.borders[3].y)),
                        (int(self.borders[0].x), int(self.borders[0].y)), 2)
    def draw_walls(self):
        #### Wall1 ####
        for i in range(len(self.wall1)-1):
            pygame.draw.line(self.win, (255, 0, 0), (int(self.wall1[i].x), int(self.wall1[i].y)),
                             (int(self.wall1[i + 1].x), int(self.wall1[i + 1].y)), 2)
        #### Wall2 ####
        for i in range(len(self.wall2)-1):
            pygame.draw.line(self.win, (255, 0, 0), (int(self.wall2[i].x), int(self.wall2[i].y)),
                             (int(self.wall2[i + 1].x), int(self.wall2[i + 1].y)), 2)


    def update_screen(self, x, y, angle, radius, deltaT):
        ### Draw robot ###
        pygame.draw.circle(self.win, (0, 255, 0), (int(x), int(y)), radius)

        pygame.draw.line(self.win, (255, 255, 0), (int(x), int(y)),
                         (x + radius * -np.cos(angle), (y + radius * np.sin(angle))),
                         int(radius / 10))

        pygame.time.delay(deltaT)
        pygame.display.update()


    def quit_screen(self):
        pygame.quit()