import pygame
import math
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 800))
done = False
is_blue = True
x = 30
y = 30
radium=30
clock = pygame.time.Clock()

vr=2
vl=4

def calspeed(vr, vl):
    v= (vr + vl) / 2
    return v

l = radium

def calr(vr, vl, l):
    r= 1/2 * l * (vr + vl) / (vr - vl)
    return r

def calw(vr, vl, l):
    w = (vr - vl) / l
    return w

r = calr(vr, vl, l)
angle = np.pi/2
w = calw(vr, vl, l)
def calicc(x, y, r, angle):
    icc = np.array([x - r * math.sin(angle), y + r * math.cos(angle)])
    return icc

icc = calicc(x, y, r, angle)

def calpose(x, y, icc, w, angle,time_step, t):
    mtx1 = np.array([[math.cos(w * time_step * t), -math.sin(w * time_step * t), 0],
              [math.sin(w * time_step * t), math.cos(w * time_step * t), 0],
              [0, 0, 1]])
    mtx2 = np.array([[x - icc[0]],
                    [y - icc[1]],
                    [angle]])
    mtx3 = np.array([[icc[0]],
                    [icc[1]],
                    [w * time_step * t]])
    mtx4 = np.matmul(mtx1, mtx2) + mtx3
    
    return float(mtx4[0]), float(mtx4[1]), float(mtx4[2])

time_step=5
t = 10

newx, newy, newangle = calpose(x, y, icc, w, angle,time_step, t)

while not done:
    
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        is_blue = not is_blue
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: y -= 3
        if pressed[pygame.K_DOWN]: y += 3
        if pressed[pygame.K_LEFT]: x -= 3
        if pressed[pygame.K_RIGHT]: x += 3
#        if pressed[pygame.K_w]: vl += 2
#        if pressed[pygame.K_s]: vl -= 2
#        if pressed[pygame.K_o]: vr += 2
#        if pressed[pygame.K_l]: vr += 2
#        if pressed[pygame.K_o]: vr = vl = 0
#        if pressed[pygame.K_t]: vr += 2, vl +=2        
#        if pressed[pygame.K_t]: vr -= 2, vl -=2         
        screen.fill((0, 0, 0))
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.circle(screen, color, (x,y), radium)
        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
print('here')