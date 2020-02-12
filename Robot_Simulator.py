import pygame
import math
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 800))
done = False
x = 30
y = 30
radius=20

clock = pygame.time.Clock()


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

def UpdateState(x, y, vr, vl, deltat, l, theta):
    
    if vr == vl:
        newx = x + vr * deltat
        newy = y + vr * deltat
        newtheta = theta
    elif vr == -vl:
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
    return round(newx), round(newy), newtheta

###################Initilization####################
x = y = 30
vr = vl = 1
deltat=1
l = radius/2
theta = 0
increment = 1


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
    if pressed[pygame.K_l]: vr += increment
    if pressed[pygame.K_x]: vr = vl = 0
    if pressed[pygame.K_t]: vr += increment; vr += increment 
    if pressed[pygame.K_g]: vr -= increment; vr -= increment     
    
    #Display
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (173, 255, 47), (x, y), radius)
    endpoint=np.array([x+radius*math.sqrt(2)/2, y+radius*math.sqrt(2)/2])
    pygame.draw.line(screen, (0, 0, 0), (x, y), (endpoint[0], endpoint[1]))
    pygame.display.flip()
    clock.tick(60)
    x, y, theta = UpdateState(x, y, vr, vl, deltat, l, theta)
    
#    t+=1

pygame.quit()
print('here')