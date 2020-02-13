import pygame
import math
import numpy as np
from utils import *

w_width = 800
w_height = 800
walls_thickness = 20

pygame.init()
screen = pygame.display.set_mode((w_height, w_width))
done = False
x = 30
y = 30
radius=20


clock = pygame.time.Clock()


################# RGB Colors #################


BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (13, 255, 0)


##############################################


def calpose(x, y, r, w, theta, deltat):
    
    icc = np.array([x - r * math.sin(theta), y + r * math.cos(theta)])
    
    mtx1 = np.array([[math.cos(w * deltat), -math.sin(w * deltat), 0],
              [math.sin(w * deltat), math.cos(w * deltat), 0],
              [0, 0, 1]])
    mtx2 = np.array([[x - icc[0]],
                    [y - icc[1]],
                    [theta]])
    mtx3 = np.array([[icc[0]],
                    [icc[1]],
                    [w * deltat]])
    mtx4 = np.matmul(mtx1, mtx2) + mtx3
    
    return float(mtx4[0]), float(mtx4[1]), float(mtx4[2])

def UpdateState(x, y, vr, vl, r, deltat, l, theta):
    
    if vr == vl:
        newx = x + vr * deltat
        newy = y + vr * deltat
        newtheta = theta
    elif vr == -vl:
        r = 0
        w  = (vr - vl) / l
        theta = w * deltat
        newx, newy, newtheta = calpose(x, y, r, w, theta, deltat)
    elif vl == 0:
        r = 2/l
        w = (vr - vl) / l
        newx, newy, newtheta = calpose(x, y, r, w, theta, deltat)
    elif vr == 0:
        r = 2/l
        w = (vr - vl) / l
        newx, newy, newtheta = calpose(x, y, r, w, theta, deltat)
    else:
        r = 1/2 * l * (vr + vl) / (vr - vl)
        w = (vr - vl) / l
        newx, newy, newtheta = calpose(x, y, r, w, theta,deltat)
    return newx, newy, newtheta

###################Initilization####################
x = y = int(w_width/2)
vr = vl = 0
deltat = 1
l = radius/2
theta = 180
increment = 0.1
r=0


################### Walls #######################


#pygame.display.

borders = [
    pygame.Rect(0, 0, w_width, walls_thickness), 
    pygame.Rect(0, 0, walls_thickness, w_height), 
    pygame.Rect(0, w_width-walls_thickness, w_width, walls_thickness), 
    pygame.Rect(w_height-walls_thickness, 0, walls_thickness, w_height), 
]


endpoint=np.array([x+radius*math.sqrt(0)/2, y+radius*math.sqrt(0)/2])



##################Display###########################
while not done:
#    x = round(v*t)
#    y = round(v*t)
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
                    
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]: vl += increment
    if pressed[pygame.K_s]: vl -= increment
    if pressed[pygame.K_o]: vr += increment
    if pressed[pygame.K_l]: vr -= increment
    if pressed[pygame.K_x]: vr = vl = 0
    if pressed[pygame.K_t]: vr += increment; vl += increment
    if pressed[pygame.K_g]: vr -= increment; vl -= increment
    
    vr = np.round(vr,2); vl = np.round(vl,2)
    
    #Display
    screen.fill((255, 255, 255))
    for border in borders:
        pygame.draw.rect(screen, BLACK, border)
    pygame.draw.circle(screen, (173, 255, 47), (int(x), int(y)), radius)
    
    
    pygame.draw.circle(screen, (173, 255, 47), (int(x), int(y)), radius)
    endpoint=np.array([x+radius*math.sqrt(2)/2, y+radius*math.sqrt(2)/2])
    
    newX = x + (endpoint[0] - x) * np.cos(theta) - (endpoint[1] - y) * np.sin(theta)
    newY = y + (endpoint[0] - x) * np.sin(theta) - (endpoint[1] - y) * np.cos(theta)
    
    pygame.draw.line(screen, (0, 0, 0), (x, y), (endpoint[0], endpoint[1])) #(newX, newY))
    pygame.display.flip()
    clock.tick(60)
    x, y, theta = UpdateState(x, y, vr, vl, r, deltat, l, theta)
    print(vr, '........', vl)
    
#    t+=1

pygame.quit()
print('here')