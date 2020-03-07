# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 17:27:13 2020

@author: ammar
"""

import pygame
from pygame import Color
from pygame.math import Vector2
import math
import numpy as np
from shapely.geometry import *
from utils import *
from NeuralNetwork import NeuralNetwork

import matplotlib as mpl
import matplotlib.pyplot as plt
import time
#from sympy import * #Point, intersection
#from geometer.point import *
#from geometer.shapes import *

pygame.init()


w_width = 800
w_height = 800
walls_thickness = 20

win = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('Simulator')

x = 50
y = w_height/2

bot_c = Point(x,y)
angle = math.radians(0)
radius = 20
length = 2*radius
sens_l = 200#3*radius

nb_sensors = 12

v_l = 0
v_r = 0
run = True
w_pressed = False
s_pressed = False

tst = False
no_paricles = 100
radius_dust = 2
particles_cleared = 0
max_iters_pergen = 100

################## Numbers ###################

n_gen = 10          
n_pop = 10

##############################################
################# RGB Colors #################

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (13, 255, 0)
GREEN = Color("purple")
YELLOW = (255, 255, 0)
SENS_RED = (255,0,0)
BG_COLOR = Color("lightblue")

##############################################



################# Functions ##################

def fitness_function(particles_cleared,sensor_distances,collision_count,timestep,v_l,v_r,fitness):
	dist_threshold = 10
	terminate = False
	np_distances = np.asarray(sensor_distances)
	np_distances = np.where((np_distances > 10) & (np_distances < 40), 1, 0)
	closer_wall_factor = np.sum(np_distances)/12
	fitness += (4 * particles_cleared  + 2 * closer_wall_factor - 4 * collision_count) * ((abs(v_l) + abs(v_r))/2)
	if(timestep%30 == 0):
		prev_v_l = v_l
		prev_v_r = v_r
		prev_fitness = fitness
		if(prev_fitness < 0 and fitness < 0):
			terminate = True
		if(prev_v_l == 0 and prev_v_r == 0 and v_l == 0 and v_r == 0):
			terminate = True
	return fitness, terminate

	

def CreateDust(no_paricles,width,height):
	random_coord = np.random.rand(no_paricles,2)
	random_coord[ : ,0] = random_coord[ : ,0] * width
	random_coord[ : ,1] = random_coord[ : ,1] * height
	return random_coord

def CalculateDistance(dust_positions,center_bot):
	return  np.array([distance(dust_position,center_bot) for dust_position in dust_positions])

def Clear_Dust(dust_positions,radius_dust,radius_circle,dust_distances):
	initial_dust_count = len(dust_positions)
	colliding_dust_indices = np.argwhere(dust_distances <= radius_dust + radius_circle)
	dust_positions = np.delete(dust_positions,colliding_dust_indices,0)
	after_dust_count = len(dust_positions)
	return dust_positions,initial_dust_count - after_dust_count

def create_font(t,s=15,c=(0,0,0), b=False,i=False):
    font = pygame.font.SysFont("Arial", s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text

def createWorld():
    return

def createBot():
    return
#dist_text = create_font(tt)


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


def sensing(sensor, angle):
    detect = False
    dist = sens_l - radius
    inter_pt = None
    
    for border in borders_line:
        test1 = line_top.intersection(sensor)
        test2 = line_right.intersection(sensor)
        test3 = line_bottom.intersection(sensor)
        test4 = line_left.intersection(sensor)
        test5 = test_line1.intersection(sensor)
        test6 = test_line2.intersection(sensor)
        if not (test1.is_empty):
#            print("Sensor {} intersects with {} at: {}".format(sensor, border, test1))
            detect = True
            inter_pt = test1
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test2.is_empty):
#            print("Sensor {} intersects with {} at: {}".format(sensor, border, test1))
            detect = True
            inter_pt = test2
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test3.is_empty):
#            print("Sensor {} intersects with {} at: {}".format(sensor, border, test1))
            detect = True
            inter_pt = test3
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test4.is_empty):
#            print("Sensor {} intersects with {} at: {}".format(sensor, border, test1))
            detect = True
            inter_pt = test4
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test5.is_empty):
#            print("Sensor {} intersects with {} at: {}".format(sensor, border, test1))
            detect = True
            inter_pt = test5
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test6.is_empty):
#            print("Sensor {} intersects with {} at: {}".format(sensor, border, test1))
            detect = True
            inter_pt = test6
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])

    return detect, dist, inter_pt
        

def Collision(center,radius,start_point,end_point):	
    along_vector = end_point - start_point	
    a = along_vector.dot(along_vector)	
    b =  2 * along_vector.dot(start_point - center)	
    c = start_point.dot(start_point) + center.dot(center) - 2 * start_point.dot(center) - radius**2	
    disc = b**2 - 4*a*c	
    if(disc< 0 ):	
        #print('Line missing the circle')	
        return False	
    sqrt_disc = math.sqrt(disc)	
    t1 = (-b + sqrt_disc) / (2 * a)	
    t2 = (-b - sqrt_disc) / (2 * a)	
    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):	
        #print('line would hit the circle if extended')	
        return False	
    t = max(0, min(1, - b / (2 * a)))	
    return True	

def distance(p1,p2):	
    return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )	

def Slope(point1, point2,point3,point4):	
    x1,y1 = point1
    x2,y2 = point2
    dy = y2 - y1
    dx = x2 -x1
    x3,y3 = point3
    x4,y4 = point4
    dy2 = y4 - y3
    dx2 = x4 -x3
    if(dx == 0 and dx2 == 0):
        return 0
    elif(dx == 0):
        slope2 = dy2/dx2
        if dy>=0:
            return np.pi/2 - math.atan(slope2)
        else:
            return -np.pi/2 - math.atan(slope2)
    elif(dx2 == 0):
        slope1 = dy/dx
        if dy2>=0:
            return np.pi/2 - math.atan(slope1)
        else:
            return -np.pi/2 - math.atan(slope1)
    slope1 = dy/dx
    slope2 = dy2/dx2
    tan_angle = (slope1-slope2)/(1+slope1*slope2)
    return math.atan(tan_angle)
    

def drawWalls():
    borders = [
        pygame.Rect(0, 0, w_width, walls_thickness), 
        pygame.Rect(0, 0, walls_thickness, w_height), 
        pygame.Rect(0, w_width-walls_thickness, w_width, walls_thickness), 
        pygame.Rect(w_height-walls_thickness, 0, walls_thickness, w_height), 
        ]
    
    for border in borders:
        pygame.draw.rect(win, BLACK, border)

    borders_line = [
        pygame.draw.line(win, RED, line_top.bounds[0:2], line_top.bounds[2:4],2),
        pygame.draw.line(win, RED, line_right.bounds[0:2], line_right.bounds[2:4],2),
        pygame.draw.line(win, RED, line_bottom.bounds[0:2], line_bottom.bounds[2:4],2),
        pygame.draw.line(win, RED, line_left.bounds[0:2], line_left.bounds[2:4],2),
        pygame.draw.line(win, Color('orange'), test_line1.coords[0], test_line1.coords[1],4),
        pygame.draw.line(win, Color('purple'), test_line2.coords[0], test_line2.coords[1],4),
        
        ]

    return borders, borders_line

def collisionMovement(v_r, v_l, angle, theta):
#    if angle < 0:
#        angle += 2 * np.pi
#    if angle > np.pi/2 :
#        angle = np.pi - angle
    velocity = (v_r + v_l)/2
    new_x = np.cos(angle + np.pi)*np.cos(theta)*velocity
    new_y = np.sin(angle + np.pi)*np.sin(theta)*velocity
#   v_x = velocity * -np.cos(angle)
#   v_y = velocity * np.sin(angle)
    
#   v_wall = v_x * np.sin(angle) * np.cos(theta) + v_y * -np.cos(angle) * np.sin(theta)
#    v_nall = 0
    return new_x, new_y
#    return (v_wall * np.cos(theta)), (v_wall * np.sin(theta))

def drawSensors():
    
    sensors_lines = []    
    sensors = []
    distances = [None] * 12

    for i in range(nb_sensors):
        sensors_lines.append(LineString(
                                        [bot_c, (bot_c.x + sens_l * -np.cos(angle + np.radians((i * 360/nb_sensors))),
                                                 (bot_c.y + sens_l * np.sin(angle + np.radians((i * 360/nb_sensors)))))]
                                        )
                            )
    for i in range(len(sensors_lines)):
        det, dist, int_pt = sensing(sensors_lines[i], angle)      # returns 3 values ('detection (bool)', 'distance (value)', 'Intersection point(Point)')
        distances[i] = dist
#        print("Distance for sensor {}, = {}".format(i, dist))
        
        #### TODO TEXT HERE
        ###
        if det:
            sensors.append(
#                    pygame.draw.line(win, GREEN, (int(x), int(y)), (x + sens_l * -np.cos(angle + np.radians(i * 360/nb_sensors)),
#                                          (y + sens_l * np.sin(angle + np.radians(i * 360/nb_sensors))))),
#                    )  
                    pygame.draw.line(win, Color("darkgreen"), (int(x), int(y)), (int_pt.x, int_pt.y),2),
                    )  
            txt = create_font(str(round(dist,0)))
            win.blit(txt,  (int_pt.x, int_pt.y))

        else:
            sensors.append(
                    pygame.draw.line(win, SENS_RED, (int(x), int(y)), (x + sens_l * -np.cos(angle + np.radians(i * 360/nb_sensors)),
                                          (y + sens_l * np.sin(angle + np.radians(i * 360/nb_sensors))))),
                    )
            if not tst:
                txt = create_font(str(round(dist,0)))
                win.blit(txt, (x + sens_l * -np.cos(angle + np.radians(i * 360/nb_sensors)),
                                              (y + sens_l * np.sin(angle + np.radians(i * 360/nb_sensors)))))

            
    return distances

def drawspeeds():
    left_wheel_text = create_font(str(round(v_l)))
    win.blit(left_wheel_text, (x + radius * -np.cos(angle + np.pi/2),(y + radius * np.sin(angle + np.pi/2))))
    right_wheel_text = create_font(str(round(v_r)))
    win.blit(right_wheel_text, (x + radius * -np.cos(angle - np.pi/2), (y + radius * np.sin(angle - np.pi/2))))
    return()
    
    
####################### NN ##########################
def initWeights():
    weight_l1 = np.random.randn(6,12)
    weight_l2 = np.random.randn(2,6)
    bias = np.random.randn()
    bias2 = np.random.randn()
    
    return weight_l1, weight_l2, bias, bias2

def feedForward(x, weight_l1, weight_l2, bias, bias2):
    h1 = np.dot(weight_l1, x.T) + bias
    a1 = np.tanh(h1)
    h2 = np.dot(weight_l2, a1.T) + bias2
    output = np.tanh(h2)
    return output
#####################################################



################ Walls & Sensors ####################
margin = 20
b1_s = Point(0 + margin, 0 + margin)
b1_e = Point(w_width - margin, 0 + margin)
b2_s = Point(w_width - margin, 0 + margin)
b2_e = Point(w_width - margin, w_height - margin)
b3_s = Point(w_width - margin, w_height - margin)
b3_e = Point(0 + margin, w_height - margin)
b4_s = Point(0 + margin, w_height - margin)
b4_e = Point(0 + margin, 0 + margin)

start_pointP = Point(0,2) #### DEFINE THE LEFT MOST POINT AS END POINT
end_pointP = Point(2,2) #### DEFINE THE RIGHT MOST POINT AS START POINT
end_pointP2 = Point(0,2)
start_pointP2 = Point(2,2)


# TODO: CHANGE EVERYTHING TO POINT
b1_sv = Vector2(0 + margin, 0 + margin)
b1_ev = Vector2(w_width - margin, 0 + margin)
b2_sv = Vector2(w_width - margin, 0 + margin)
b2_ev = Vector2(w_width - margin, w_height - margin)
b3_sv = Vector2(w_width - margin, w_height - margin)
b3_ev = Vector2(0 + margin, w_height - margin)
b4_sv = Vector2(0 + margin, w_height - margin)
b4_ev = Vector2(0 + margin, 0 + margin)


start_point = Vector2(0, 2) #### DEFINE THE LEFT MOST Vector2 AS END Vector2
end_point = Vector2(2,2) #### DEFINE THE RIGHT MOST Vector2 AS START Vector2
end_point2 = Vector2(2,2)
start_point2 = Vector2(0,2)

line_top = LineString([b1_s, b1_e])
line_right = LineString([b2_s, b2_e])
line_bottom = LineString([b3_s, b3_e])
line_left = LineString([b4_s, b4_e])

test_line1 = LineString([start_pointP, end_pointP])
test_line2 = LineString([start_pointP2, end_pointP2])


################# INITIALIZATION ##################

borders, borders_line = drawWalls()
distances = drawSensors()
bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle),
                                          (bot_c.y + radius * np.sin(angle)))]) #, int(radius/10))
###################################################
            
            
    
################# Define collison lines here #######################
collison_walls = [
        [b1_sv, b1_ev],
        [b2_sv, b2_ev],
        [b3_sv, b3_ev],
        [b4_sv, b4_ev],
        [start_point,end_point],
        [start_point2, end_point2]
        ]
####################################################################
################### ------- MAIN LOOP ------- ######################
dust_positions = CreateDust(no_paricles,w_width - walls_thickness,w_height - walls_thickness)
timestep = 0
fitness = 0
        
w1, w2, b1, b2 = initWeights()

while run:
    for gen in range(n_gen):
        print("Generation: ", gen)
        for pop in range(n_pop):
            print("Population: ", pop)
            for t in range(max_iters_pergen):
                pygame.time.delay(60)                  
                ##### 
                t_v_r, t_v_l = feedForward(np.asarray(distances), w1, w2, b1, b2)
                
                v_r += t_v_r
                v_l += t_v_l
                
                if(v_r > 0):
                    v_r = np.min([v_r, 30])
                else:
                    v_r = np.max([v_r, -30])
                if(v_l > 0):
                    v_l = np.min([v_l, 30])
                else:
                    v_l = np.max([v_l, -30])
                            
                ### Redraw
                win.fill((BG_COLOR))
                borders, borders_line = drawWalls()
            
                #### Draw Dust
                distance_dust = CalculateDistance(dust_positions,(x,y))
                dust_positions,count_cleared = Clear_Dust(dust_positions,radius,radius_dust,distance_dust)
                particles_cleared += count_cleared
                for i in range(len(dust_positions)):
                		pygame.draw.circle(win,BLACK,(int(dust_positions[i,0]),int(dust_positions[i,1])),radius_dust)
            
                #### Collision stuff ######
                
                
                
                next_angle, next_x, next_y = ICC_Calculation2(v_r, v_l, radius, angle, x, y)	
                
                
                
                center = Vector2(next_x,next_y)
                end_line = Vector2(next_x + radius * -np.cos(next_angle),y + radius * np.sin(next_angle))	
                collision_count = 0	
                absolute_velocity = (v_r + v_l)/2	
                colliding_walls = []	
                for i in range(len(collison_walls)):	
                    if(Collision(center,radius,collison_walls[i][0],collison_walls[i][1]) == True):	
                        collision_count +=1	
                        colliding_walls.append(collison_walls[i])            
                if(collision_count == 0):	
                    angle,x,y = next_angle,next_x,next_y	
                    distances = drawSensors()
                    pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
                    bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle),
                                                  (bot_c.y + radius * np.sin(angle)))]) #, int(radius/10))    pygame.draw.line(win, YELLOW, bot_line.bounds[0:2], bot_line.bounds[2:4], int(radius/10))         # surface to draw on, color, s_pt, e_pt, width
                    line = pygame.draw.line(win, YELLOW, (x, y), (x + radius * -np.cos(angle),(y + radius * np.sin(angle))), int(radius/10))
                    drawspeeds()
                    bot_c = Point((x), (y))
                elif(collision_count == 1):
                    if (colliding_walls[0][1].x - colliding_walls[0][0].x) == 0:
                        theta = np.pi/2
                    else:
                        theta = math.atan((colliding_walls[0][1].y - colliding_walls[0][0].y)/(colliding_walls[0][1].x - colliding_walls[0][0].x))
                   
            #        print("Theta: {}".format(theta))
                    x_offset, y_offset = collisionMovement(v_r, v_l, angle, theta)
                    x = x + x_offset
                    y = y - y_offset
                    distances = drawSensors()
                    pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
                    bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle),
                                                  (bot_c.y + radius * np.sin(angle)))]) #, int(radius/10))    pygame.draw.line(win, YELLOW, bot_line.bounds[0:2], bot_line.bounds[2:4], int(radius/10))         # surface to draw on, color, s_pt, e_pt, width
                    line = pygame.draw.line(win, YELLOW, (x, y), (x + radius * -np.cos(angle),(y + radius * np.sin(angle))), int(radius/10))
                    drawspeeds()
                    bot_c = Point((x), (y))
                else:
                    distances = drawSensors()
                    pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
                    line = pygame.draw.line(win, YELLOW, (x, y), (x + radius * -np.cos(angle),(y + radius * np.sin(angle))), int(radius/10))
                    drawspeeds()
                ###########################
                # Update / Call next tick #
            
                if angle > 2*np.pi : 
                    angle = angle - 2*np.pi
                elif angle < -2*np.pi:
                    angle = angle + 2*np.pi
                timestep = timestep+1
                fitness,terminate = fitness_function(count_cleared,distances,collision_count,timestep,v_l,v_r,fitness)
            #    print(fitness)
                if(timestep == max_iters_pergen):
                    dust_positions = CreateDust(no_paricles,w_width - walls_thickness,w_height - walls_thickness)
                pygame.display.update()

run = False        
###################################################
print("Cleared particles: {}".format(particles_cleared))
pygame.quit()