import pygame
from pygame.math import Vector2
import math
import numpy as np
from shapely.geometry import *

pygame.init()


w_height = 800
w_width = 800
walls_thickness = 20

win = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('Simulator')

x = w_width/2
y = w_height/2
angle = math.radians(-90)
radius = 30
length = 2*radius
sens_l = 3*radius

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


#def calcSlope(sp, ep):      # start / end point of line
#   # Ensure that the line is not vertical
#   if (sp[0] != ep[0]):
#       # slope
#       return (sp[1] - ep[1]) / (sp[0] - ep[0])
#   else:
#       return None

def line_intersect(sens_line, target_line, angle):
    intersection = False
    # Returns point of intersection between both lines
    d_x = (sens_line.x - sens_line.x + sens_l * -np.cos(angle),
           target_line.x - target_line.x + 760)
    d_y = (sens_line.y - sens_line.y + sens_l * np.sin(angle),
           target_line.y - target_line.y)
    print("target line x +: {}".format(target_line.x + 760))
    
    
#    (x + sens_l * -np.cos(angle),(y + sens_l * np.sin(angle))))
    
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
    
    
    div = det(d_x, d_y)
    if div != 0:
        d = (det((sens_line.x, sens_line.x + sens_l * -np.cos(angle)), 
                 (sens_line.y, sens_line.y + sens_l * np.sin(angle))),
            det((target_line.x, target_line.x + 760), (target_line.y, target_line.y)))
        x_intersect = det(d, d_x) / div
        y_intersect = det(d, d_y) / div
        intersection = True
        print("Intersection of sensor {} with line from {}, at {}".format(sens_line, 
                                                                          target_line, 
                                                                          (x_intersect, y_intersect)))
        return x_intersect, y_intersect, intersection
    else:
        return None, None, None
        
#    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
#    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
#
#    def det(a, b):
#        return a[0] * b[1] - a[1] * b[0]
#
#    div = det(xdiff, ydiff)
#    if div == 0:
#       raise Exception('lines do not intersect')
#
#    d = (det(*line1), det(*line2))
#    x = det(d, xdiff) / div
#    y = det(d, ydiff) / div
#    return x, y

def intersectionPoint(sens_coord, target_coord):
    line1 = LineString(sens_coord)
    line2 = LineString((target_coord[0],target_coord[1]))
    print("LINE1: {} \nLINE2: {}".format(sens_coord, target_coord))
    return (line1.intersection(line2))

def sensing(sensor, angle):
    detect = False
    dist = 0
    
#    for border in borders_line:
#    x_int, y_int, detect = line_intersect(sensor, borders_line[0], angle)
    
    int_coord = intersectionPoint(((sensor.x,sensor.y),                     # start x/y of sensor
                                   (sensor.x + sens_l * -np.cos(angle),     # end x of sensor
                                    sensor.y + sens_l * np.sin(angle))),    # end y of sensor
                                    (b1_s,b1_e))                            # start / end coords of top wall
    
#    if int_coord != None:
#        detect = true
    
    if int_coord != None:
        detect = True
        print("Distance to intersection point: {}".format(int_coord))
        print("Sensor {} sees something: {}\n At:{}".format(sensor, detect, int_coord))
    return detect, dist
        
        
#        (x - R(v_r, v_l, l) * np.sin(theta)), (y - R(v_r, v_l, l) * np.cos(theta))
        
        
################ Walls & Sensors ####################
b1_s = Vector2(20, 20)
b1_e = Vector2(780, 20)
b2_s = Vector2(780, 20)
b2_e = Vector2(780, 780)
b3_s = Vector2(780, 780)
b3_e = Vector2(20, 780)
b4_s = Vector2(20, 780)
b4_e = Vector2(20, 20)

borders = [
    pygame.Rect(0, 0, w_width, walls_thickness), 
    pygame.Rect(0, 0, walls_thickness, w_height), 
    pygame.Rect(0, w_width-walls_thickness, w_width, walls_thickness), 
    pygame.Rect(w_height-walls_thickness, 0, walls_thickness, w_height), 
]

borders_line = [
    pygame.draw.line(win, RED, b1_s, b1_e),
    pygame.draw.line(win, RED, b2_s, b2_e),
    pygame.draw.line(win, RED, b3_s, b3_e),
    pygame.draw.line(win, RED, b4_s, b4_e),
        ]
sensors2 = [
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
            pygame.Rect((x, y),(1,sens_l)),
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

    borders_line = [
        pygame.draw.line(win, RED, b1_s, b1_e),
        pygame.draw.line(win, RED, b2_s, b2_e),
        pygame.draw.line(win, RED, b3_s, b3_e),
        pygame.draw.line(win, RED, b4_s, b4_e),
        ]
         

    sensors = [
        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle),
                                      (y + sens_l * np.sin(angle)))),
#        
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(30)),
#                                      (y + sens_l * np.sin(angle + np.radians(30))))),
#        
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(60)),
#                                      (y + sens_l * np.sin(angle + np.radians(60))))),
#        
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(90)),
#                                      (y + sens_l * np.sin(angle + np.radians(90))))),
#        
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(120)),
#                                      (y + sens_l * np.sin(angle + np.radians(120))))),
#        
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(150)),
#                                      (y + sens_l * np.sin(angle + np.radians(150))))),
#        
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(180)),
#                                      (y + sens_l * np.sin(angle + np.radians(180))))),
##        
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(210)),
#                                      (y + sens_l * np.sin(angle + np.radians(210))))),
#        
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(240)),
#                                      (y + sens_l * np.sin(angle + np.radians(240))))),
#                                    
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(270)),
#                                      (y + sens_l * np.sin(angle + np.radians(270))))), 
#                                    
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(300)),
#                                      (y + sens_l * np.sin(angle + np.radians(300))))),
#                                                                            
#        pygame.draw.line(win, RED, (x, y), (x + sens_l * -np.cos(angle + np.radians(330)),
#                                      (y + sens_l * np.sin(angle + np.radians(330))))),
        ] 
    
    
    for sensor in sensors:
        sensing(sensor, angle)
        
#    for sensor in sensors2:
#        sensor.rotate(win, angle)
    circle = pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
#    print("print: {}".format(x + radius * np.cos(angle)))
    line = pygame.draw.line(win, BLACK, (x, y), (x + radius * -np.cos(angle),
                                          (y + radius * np.sin(angle))), int(radius/10))
    
   
    angle, x, y = ICC_Calculation2(v_r, v_l, radius, angle, x, y)


    pygame.display.update()
pygame.quit()