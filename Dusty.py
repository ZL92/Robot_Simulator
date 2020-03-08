# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 11:55:28 2020

@author: ammar
"""

################################ Imports ######################################

import pygame
import math
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pygame import Color
from pygame.math import Vector2
from shapely.geometry import *
from utils import *
from pygame.locals import *
from copy import copy, deepcopy
from all_functions import * 
##############

############################### Parameters ####################################


w_width = 800
w_height = 800
walls_thickness = 20
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
no_paricles = 300
radius_dust = 2
particles_cleared = 0
max_iters_pergen = 200
prev_v_r = 0
prev_v_l = 0
prev_fitness = 0

################## Numbers ###################

n_gen = 30         
n_pop = 10

########### EA ##################
keep_n = 3
#################################
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


##############


############################# World building ##################################

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

borders, borders_line = drawWalls(w_width, w_height, walls_thickness, win)
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

##############


################### ------- MAIN LOOP ------- ######################

pygame.init()
win = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('Simulator')

np.random.seed(0)
dust_positions = CreateDust(no_paricles,w_width - walls_thickness,w_height - walls_thickness)
timestep = 0
fitness = 0
w1_pop = np.random.randn(n_pop, 6, 12)
w2_pop = np.random.randn(n_pop, 2, 6)
b1_pop = np.random.randn(n_pop,1)
b2_pop = np.random.randn(n_pop,1)
recurrent1 = np.random.randn(6,1)
fit_pop = np.empty((0,1))
best_size = int(n_pop/5)
#print("Weights: ", weights)
#print("weights0", weights[0])
print(fit_pop)
while run:
    for gen in range(n_gen):                # After each Gen: Sel, Rep, Sel/Mut
        print("Generation: ", gen)
        fit_pop = np.empty((0,1))
        for pop in range(n_pop):
            particles_cleared = 0
            x, y = (100,400)
            w1, w2, b1, b2 = w1_pop[pop], w2_pop[pop], b1_pop[pop], b2_pop[pop]
            pygame.init()
            print("Population: ", pop)
            for t in range(max_iters_pergen):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                pygame.time.delay(10)   
                
                ##### 
                distances = np.asarray(distances)/180
                t_v,t_r_1,swap = feedForward(np.asarray(distances), w1, w2, b1, b2,recurrent1,t)
                if swap:
                	recurrent1 = t_r_1
                t_v_r,t_v_l = t_v
                v_r = t_v_r * 30
                v_l = t_v_l * 30
                
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
                borders, borders_line = drawWalls(w_width, w_height, walls_thickness, win)
            
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
                if(terminate):
                    break
                pygame.display.update()
            print(fitness)
            dust_positions = CreateDust(no_paricles,w_width - walls_thickness,w_height - walls_thickness)
            fit_pop = np.append(fit_pop, fitness)
            fitness = 0
        #### Selection
        print("Fitness pop array: ", fit_pop)
        e_w1, e_w2, e_b1, e_b2, e_indices = TruncSelect(n_pop, keep_n, fit_pop, w1_pop, w2_pop, b1_pop, b2_pop)
        #### Reproduction
        
        #### Crossover/Mutation
        cw1, cw2, cb1, cb2 = ariCrossover(w1_pop, w2_pop, b1_pop, b2_pop, e_w1, e_w2, e_b1, e_b2, e_indices)
        
        mw1_pop, mw2_pop, mb1_pop, mb2_pop = gausMutation(cw1, cw2, cb1, cb2, e_w1, e_w2, e_b1, e_b2, e_indices)
        
        w1_pop, w2_pop, b1_pop, b2_pop = mw1_pop, mw2_pop, mb1_pop, mb2_pop
        
    run = False

run = False        
print("Fitpop", fit_pop)
###################################################
print("Cleared particles: {}".format(particles_cleared))
pygame.quit()
