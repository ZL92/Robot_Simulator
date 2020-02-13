import pygame
import math
import numpy as np
pygame.init()


w_height = 800
w_width = 800
walls_thickness = 20

win = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('Simulator')

x = w_width/2
y = w_height/2
angle = np.deg2rad(90)
radius = 25
v_l = 0
v_r = 0
run = True
w_pressed = False
s_pressed = False


################# RGB Colors #################


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (13, 255, 0)

##############################################


################# Functions ##################

def ICC_Calculation():
    global v_l, v_r, radius, angle, x, y
#    print("angle: {}".format(angle))
    if v_l - v_r != 0:
        icc_distance = (radius)*(v_r + v_l)/(v_r - v_l)         
        omega = (v_r - v_l)/(2*radius)
        icc_x = x - (icc_distance * np.sin(angle))
        icc_y = y - (icc_distance * np.cos(angle))
        
        icc_x, icc_y = (x - icc_distance * np.sin(angle)), (y - icc_distance * np.cos(angle))
        
        a = np.matrix([ [np.cos(omega),  -np.sin(omega), 0], 
                        [np.sin(omega), np.cos(omega),  0], 
                        [0,             0,              1]])
    
        b = np.array([x - icc_x, 
                      y - icc_y, 
                      angle]).T
    
        c = np.array([icc_x, 
                      icc_y, 
                      omega]).T
    
    
        output_vector = np.dot(a, b) + c
        
        x = output_vector[0, 0]
        y = output_vector[0, 1]
        angle = output_vector[0, 2]
#        print("angle2: {}".format(angle))
    if v_l == v_r:
        x = x + v_r * np.cos(angle)
        y = y + v_r * np.sin(angle)
        
        
#        (x - R(v_r, v_l, l) * np.sin(theta)), (y - R(v_r, v_l, l) * np.cos(theta))
        
        
################### Walls #######################

borders = [
    pygame.Rect(0, 0, w_width, walls_thickness), 
    pygame.Rect(0, 0, walls_thickness, w_height), 
    pygame.Rect(0, w_width-walls_thickness, w_width, walls_thickness), 
    pygame.Rect(w_height-walls_thickness, 0, walls_thickness, w_height), 
]

###################################################

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == 119:
                v_l += 1
            if event.key == 115:
                v_l -= 1
            if event.key == 111:
                v_r += 1
            if event.key == 108:
                v_r -= 1
            if event.key == 120:
                v_r = 0
                v_l = 0
            if event.key == 116:
                v_l += 1
                v_r += 1
            if event.key == 103:
                v_r -= 1
                v_l -= 1
    win.fill((WHITE))
    for border in borders:
        pygame.draw.rect(win, BLACK, border)
    # oldx = x
    # oldy = y
    ICC_Calculation()
    # if((x<25 or x>775)):
    # 	print('x border')
    # 	pygame.draw.circle(win, (255, 255, 255), (int(oldx), int(y)), radius)
	# elif((y<25 or y>775)):
	# 	print('Y border')
	# 	pygame.draw.circle(win, (255, 255, 255), (int(x), int(oldy)), radius)
	# else:
    pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
    pygame.draw.line(win, BLACK, (x, y), (x+radius*np.cos(angle), y+radius*np.sin(angle)))
    
#    #left wheel
#    pygame.draw.line(win, RED, (x-radius, y), (x+radius*np.cos(angle)-radius, y+radius*np.sin(angle)))
#    #right wheel
#    pygame.draw.line(win, RED, (x+radius, y), (x+radius*np.cos(angle), y+radius*np.sin(angle)))
    pygame.display.update()
pygame.quit()