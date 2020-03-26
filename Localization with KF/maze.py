'''

Initilizing maze and point-based features
No walls, no collision with features
Known correspondence which means all features have unique labels
screen visualization
'''
import pygame
from visualization import *
from shapely.geometry import *


#### Variables ####
map_width = 500
map_height = 500
borders = [Point(20, 20), Point(20, map_width-20), Point(map_height-20, map_width-20), Point(map_height-20, 20), Point(20, 20)]
wall1 = [Point(20, 150), Point(350, 150), Point(350, 400), Point (250, 400)]
wall2 = [Point(150, map_height-20), Point(150, 300), Point (280, 300)]
maze = [borders, wall1, wall2]
features = [Point(20, 20), Point(20, map_width-20), Point(map_height-20, map_width-20), Point(map_height-20, 20),
            Point(20, 150), Point(350, 150), Point(350, 400), Point (250, 400),
            Point(150, map_height-20), Point(150, 300), Point (280, 300)]
testfeatures = [Point(20,map_height-20)]
beacons = [features]

def draw_borders(win):
    for i in range(len(borders) - 1):
        pygame.draw.line(win, (255, 0, 0), (int(borders[i].x), int(borders[i].y)),
                         (int(borders[i + 1].x), int(borders[i + 1].y)), 5)

def draw_walls(win):
    #### Wall1 ####
    for i in range(len(wall1)-1):
        pygame.draw.line(win, (255, 0, 0), (int(wall1[i].x), int(wall1[i].y)),
                         (int(wall1[i + 1].x), int(wall1[i + 1].y)), 2)
    #### Wall2 ####
    for i in range(len(wall2)-1):
        pygame.draw.line(win, (255, 0, 0), (int(wall2[i].x), int(wall2[i].y)),
                         (int(wall2[i + 1].x), int(wall2[i + 1].y)), 2)
        
    
def draw_beacons(win):
    for i in range(len(features)):
        pygame.draw.circle(win, (0,140,140), (int(features[i].x), int(features[i].y)), 5)


def update_screen(win, bot_c, angle, radius, deltaT=30):

    ### Draw robot ###
    pygame.draw.circle(win, (0, 255, 0), (int(bot_c.x), int(bot_c.y)), radius)
    pygame.draw.line(win, (255, 255, 0), (int(bot_c.x), int(bot_c.y)),
                     (bot_c.x + radius * -np.cos(angle), (bot_c.y + radius * np.sin(angle))),
                     int(radius / 10))
    pygame.display.update()
    pygame.time.delay(deltaT)

def quit_screen(): #TOBE TEST
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
