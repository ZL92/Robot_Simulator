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
angle = math.radians(45)
radius = 100
length = 2*radius
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

################# Inits ####################

## Initial "front" point
#pygame.draw.line(win, BLACK, (x,y), ((x + (TODO - x) * np.cos(angle) - (TODO - y) * np.sin(angle)), (y + (TODO - x) * np.sin(angle) - (TODO - y) * np.cos(angle)))


###########################################

################# Functions ##################

def ICC_Calculation():
    global v_l, v_r, radius, angle, x, y
    if v_l != v_r:
        icc_distance = (radius)*(v_l + v_r)/(v_r - v_l)         
        omega = (v_r - v_l)/(2*radius)
        icc_x = x - (icc_distance * np.sin(angle))
        icc_y = y - (icc_distance * np.cos(angle))
        
        icc_x, icc_y = (x - icc_distance * np.sin(angle)), (y - icc_distance * np.cos(angle))
        
        a = np.matrix([ [np.cos(omega), -np.sin(omega), 0], 
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
    if v_l == v_r:
        x = x + v_r * np.cos(angle)
        y = y + v_r * np.sin(angle)
#    print("angle2: {}".format(math.degrees(angle)))
        
        
def ICC_Calculation2(v_r, v_l, radius, angle, x, y):
#    global v_l, v_r, radius, angle, x, y
    if v_l != v_r:
        icc_distance = (radius)*(v_l + v_r)/(v_r - v_l)         
        omega = (v_r - v_l)/(2*radius)
        icc_x = x - (icc_distance * np.sin(angle))
        icc_y = y - (icc_distance * np.cos(angle))
        
        icc_x, icc_y = (x - icc_distance * np.sin(angle)), (y - icc_distance * np.cos(angle))
        
        a = np.matrix([ [np.cos(omega), -np.sin(omega), 0], 
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
    if v_l == v_r:
        x = x + v_r * -np.cos(angle)
        y = y + v_r * np.sin(angle)
#    print("angle2: {}".format(math.degrees(angle)))
    return angle, x, y

        
        
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
    pygame.time.delay(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
#            print(event.key)
            if event.key == 119:        # W-Key
                v_l += 1
            if event.key == 115:        # S-Key
                v_l -= 1
            if event.key == 111:        # O-Key
                v_r += 1
            if event.key == 108:        # L-Key
                v_r -= 1
            if event.key == 120:        # X-Key
                v_r = 0
                v_l = 0
            if event.key == 116:        # T-Key
                v_l += 1
                v_r += 1
            if event.key == 103:        # G-Key
                v_r -= 1
                v_l -= 1
    win.fill((WHITE))
    for border in borders:
        pygame.draw.rect(win, BLACK, border)
    # oldx = x
    # oldy = y
#    ICC_Calculation()
    # if((x<25 or x>775)):
    # 	print('x border')
    # 	pygame.draw.circle(win, (255, 255, 255), (int(oldx), int(y)), radius)
	# elif((y<25 or y>775)):
	# 	print('Y border')
	# 	pygame.draw.circle(win, (255, 255, 255), (int(x), int(old)), radius)
	# else:
    pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
#    print("print: {}".format(x + radius * np.cos(angle)))
    line = pygame.draw.line(win, BLACK, (x, y), (x + radius * -np.cos(angle),
                                          (y + radius * np.sin(angle))))
    
    angle, x, y = ICC_Calculation2(v_r, v_l, radius, angle, x, y)


    
    
#    pygame.draw.line(win, RED, (x,y), ((x + (endpoint[0] - x) * np.cos(angle - old_angle) - (endpoint[1] - y) * np.sin(angle - old_angle)), (y + (endpoint[0] - x) * np.sin(angle - old_angle) - (endpoint[1] - y) * np.cos(angle - old_angle))))
#    
#    endpoint[0] = (x + (endpoint[0] - x) * np.cos(angle - old_angle) - (endpoint[1] - y) * np.sin(angle - old_angle))
#    endpoint[1] = (y + (endpoint[0] - x) * np.sin(angle - old_angle) - (endpoint[1] - y) * np.cos(angle - old_angle))
#    
#    pygame.draw.line(win, RED, (x,y), (radius * np.cos(angle), radius * np.sin(angle)))
#    print("angle:{}".format(math.degrees(angle)))
#    #left wheel
#    pygame.draw.line(win, RED, (x-radius, y), (x+radius*np.cos(angle)-radius, y+radius*np.sin(angle)))
#    #right wheel
#    pygame.draw.line(win, RED, (x+radius, y), (x+radius*np.cos(angle), y+radius*np.sin(angle)))
    pygame.display.update()
pygame.quit()