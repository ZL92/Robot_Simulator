'''
Initilizing maze and point-based features
No walls, no collision with features
Known correspondence which means all features have unique labels

'''
import pygame
from pygame import Color
from visualization import *

class Map(object):
    def __init__(self,map_width,map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.maze = []
        self.features = []
        self.win = pygame.display.set_mode((self.map_width, self.map_height))
        pygame.display.set_caption('Simulator')

    def initilize_maze(self, maze_coordinates):
        #TODO
        return self.maze

    def initilize_features(self, feature_coordinates):
        # TODO
        return self.features

    def update_screen(self,x,y,angle,radius,win,deltaT):
        draw_robot(x,y,angle,radius,win)
        pygame.display.update()
        pygame.time.delay(deltaT)
        win.fill((Color("lightblue")))

    def quit_screen(self):
        pygame.quit()