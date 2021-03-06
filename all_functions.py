# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 11:58:12 2020

@author: ammar
"""
###############################################################################
#                                                                             #
#                                                                             #
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Functions <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #
#                                                                             #
#                                                                             #
###############################################################################
###### Imports ##########

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

   
                    ##########################################
                    #                                        #
                    #      Robot Calculations Functions      #
                    #                                        #
                    ##########################################

def ICC_Calculation2(v_r, v_l, radius, angle, x, y):
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
            detect = True
            inter_pt = test1
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test2.is_empty):
            detect = True
            inter_pt = test2
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test3.is_empty):
            detect = True
            inter_pt = test3
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test4.is_empty):
            detect = True
            inter_pt = test4
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test5.is_empty):
            detect = True
            inter_pt = test5
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
        if not (test6.is_empty):
            detect = True
            inter_pt = test6
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
    return detect, dist, inter_pt
      

def CalculateDistance(dust_positions,center_bot):
	return  np.array([distance(dust_position,center_bot) for dust_position in dust_positions])

def Collision(center,radius,start_point,end_point):	
    along_vector = end_point - start_point	
    a = along_vector.dot(along_vector)	
    b =  2 * along_vector.dot(start_point - center)	
    c = start_point.dot(start_point) + center.dot(center) - 2 * start_point.dot(center) - radius**2	
    disc = b**2 - 4*a*c	
    if(disc< 0 ):	
        return False	
    sqrt_disc = math.sqrt(disc)	
    t1 = (-b + sqrt_disc) / (2 * a)	
    t2 = (-b - sqrt_disc) / (2 * a)	
    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):	
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
    
def collisionMovement(v_r, v_l, angle, theta):
    velocity = (v_r + v_l)/2
    new_x = np.cos(angle + np.pi)*np.cos(theta)*velocity
    new_y = np.sin(angle + np.pi)*np.sin(theta)*velocity
    return new_x, new_y



                    ##########################################
                    #                                        #
                    #        World Building Functions        #
                    #                                        #
                    ##########################################


def createWorld():
    return

def createBot():
    return

def CreateDust(no_paricles,width,height):
	random_coord = np.random.rand(no_paricles,2)
	random_coord[ : ,0] = random_coord[ : ,0] * width
	random_coord[ : ,1] = random_coord[ : ,1] * height
	return random_coord


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


def drawWalls(w_width, w_height, walls_thickness, win):
    borders = [
        pygame.Rect(0, 0, w_width, walls_thickness), 
        pygame.Rect(0, 0, walls_thickness, w_height), 
        pygame.Rect(0, w_width-walls_thickness, w_width, walls_thickness), 
        pygame.Rect(w_height-walls_thickness, 0, walls_thickness, w_height), 
        ]
    
    for border in borders:
        pygame.draw.rect(win, Color('black'), border)

    borders_line = [
        pygame.draw.line(win, Color('red'), line_top.bounds[0:2], line_top.bounds[2:4],2),
        pygame.draw.line(win, Color('red'), line_right.bounds[0:2], line_right.bounds[2:4],2),
        pygame.draw.line(win, Color('red'), line_bottom.bounds[0:2], line_bottom.bounds[2:4],2),
        pygame.draw.line(win, Color('red'), line_left.bounds[0:2], line_left.bounds[2:4],2),
        pygame.draw.line(win, Color('orange'), test_line1.coords[0], test_line1.coords[1],4),
        pygame.draw.line(win, Color('purple'), test_line2.coords[0], test_line2.coords[1],4),
        
        ]

    return borders, borders_line

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
        if det:
            sensors.append(
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
    
    
    
                    ##########################################
                    #                                        #
                    #          Neural Net. Functions         #
                    #                                        #
                    ##########################################


####################### NN ##########################
def initWeights():
    weight_l1 = np.random.randn(6,12)
    weight_l2 = np.random.randn(2,6)
    bias = np.random.randn()
    bias2 = np.random.randn()
    
    return weight_l1, weight_l2, bias, bias2

def feedForward(x, weight_l1, weight_l2, bias, bias2,r1,timestep):
	swap = False
	x = x.astype(np.float64)
	r1 = r1.astype(np.float64)
	if(timestep!=0 and timestep%30 == 0):
		x[0:4] += r1[0:4]
	h1 = np.dot(weight_l1, x.T) + bias
	a1 = np.tanh(h1)
	if(timestep%30 ==0):
		swap = True
		r1 = a1
	h2 = np.dot(weight_l2, a1.T) + bias2
	output = np.tanh(h2)
	return output,r1,swap



                    ##########################################
                    #                                        #
                    #      Evolutionary Algo. Functions      #
                    #                                        #
                    ##########################################

############################# Selection Methods ###############################

# Truncated rank-based selection: Selects n parents to keep for reproduction
def TruncSelect(pop_size, keep_n, fit_pop, w1_pop, w2_pop, b1_pop, b2_pop):
    """
    Select n best genes by their indices.
    
    Parameters
    ----------
    :pop_size:  Size of the population
    :keep_n:    Number of individuals to keep
    :fit_pop:   np Array containing fitness of the population
    :w1_pop:    np Array containing the first weights of the population
    :w2_pop:    np array containing the 2nd set of weights of the population
    :b1_pop:    np array containing 1st bias of the population
    :b2_pop:    np array containing 2nd bias of the population
    
    :returns:   np array of only best genes (w1, w2, b1, b2, indices)
    """
    indices = np.argpartition(fit_pop, -keep_n)[-keep_n:]
    elite_w1 = w1_pop[indices]
    elite_w2 = w2_pop[indices]
    elite_b1 = b1_pop[indices]
    elite_b2 = b2_pop[indices]
    return elite_w1, elite_w2, elite_b1, elite_b2, indices

# Proportional selection - TODO

# Rank-based selection - TODO

# Tournament selection - TODO



################################ Replacement ##################################

def Reproduction(pop_size, elite_genes, best_size):
    offspring_count = int(pop_size / len(elite_genes))
    assert type(offspring_count) == int, "WTF are u doing"
    parent_genes = (np.tile(elite_genes, (offspring_count + 1, 1)))
    parent_genes = np.resize(parent_genes, (pop_size, 2))
    return parent_genes


################################# Crossover ###################################

def Crossover(TODO, type_of_crossover):
    if type_of_crossover == 0:
        opCrossover()
    elif type_of_crossover == 1:
        uniCrossover()
    else:
        ariCrossover()
    return

# One-point crossover - select a point in genome and crossover the rest
def opCrossover():
    return

# Uniform crossover - Uniformaly swap out random pieces of genome
def uniCrossover():
    return

# Arithmetic crossover - New genome is averaged from parents
def ariCrossover(w1_pop, w2_pop, b1_pop, b2_pop, elite_w1, elite_w2, elite_b1, elite_b2, indices):
    """
    Reproduces genepool and applies arithmetic crossover
    
    Parameters
    ----------
    :w1_pop:    np array of 1st weights of whole population
    :w2_pop:    np array of 2nd weights of whole population
    :b1_pop:    np array of 1st bias of whole population
    :b2_pop:    np array of 2nd bias of whole population
    :elite_w1:  np array containing 1st weights of n best parents
    :elite_w2:  np array containing 2nd weights of n best parents
    :elite_b1:  np array containing 1st bias of n best parents
    :elite_b2:  np array containing 2nd bias of n best parents
    :indices:   np array containing indices of n best individuals
    
    :returns:   cw1, cw2, cb1, cb2 -> new population after crossover
    """
    # Copy of all 'elite' genes
    cw1 = deepcopy(elite_w1)
    cw2 = deepcopy(elite_w2)
    cb1 = deepcopy(elite_b1)
    cb2 = deepcopy(elite_b2)
    
    # While size of elite genes is smaller than original population
    # Keep randomly chosing (from elites) 2 parents to reproduce
    # Each time spawn a new individual by averaging parents genes
    while (len(cw1) < len(w1_pop)):
        father, mother = np.random.choice(indices, 2, replace=False)    
        new_indiv = [(w1_pop[father] + w1_pop[mother])/2]
        cw1 = np.concatenate((cw1, new_indiv))
        
    while (len(cw2) < len(w2_pop)):
        father, mother = np.random.choice(indices, 2, replace=False)    
        new_indiv = [(w2_pop[father] + w2_pop[mother])/2]
        cw2 = np.concatenate((cw2, new_indiv))
        
    while (len(cb1) < len(b1_pop)):
        father, mother = np.random.choice(indices, 2, replace=False)    
        new_indiv = [(b1_pop[father] + b1_pop[mother])/2]
        cb1 = np.concatenate((cb1, new_indiv))
        
    while (len(cb2) < len(b2_pop)):
        father, mother = np.random.choice(indices, 2, replace=False)    
        new_indiv = [(b2_pop[father] + b2_pop[mother])/2]
        cb2 = np.concatenate((cb2, new_indiv))
        
    # Resize population to original size (since might be bigger than original)
    cw1 = np.resize(cw1, (np.shape(w1_pop)))
    cw2 = np.resize(cw2, (np.shape(w2_pop)))
    cb1 = np.resize(cb1, (np.shape(b1_pop)))
    cb2 = np.resize(cb2, (np.shape(b2_pop)))
    
    # Return population after crossover
    return cw1 , cw2, cb1, cb2

################################# Mutation ####################################
# Mutation through gaussian noise
def gausMutation(w1_pop, w2_pop, b1_pop, b2_pop, elite_w1, elite_w2, elite_b1, elite_b2, indices):
    """
    Applies (gaussian) mutation to next generation
    
    Parameters
    ----------
    :w1_pop:    np array of 1st weights of whole population
    :w2_pop:    np array of 2nd weights of whole population
    :b1_pop:    np array of 1st bias of whole population
    :b2_pop:    np array of 2nd bias of whole population
    :elite_w1:  np array containing 1st weights of n best parents
    :elite_w2:  np array containing 2nd weights of n best parents
    :elite_b1:  np array containing 1st bias of n best parents
    :elite_b2:  np array containing 2nd bias of n best parents
    :indices:   np array containing indices of n best individuals
    
    :returns:   mw1_pop, mw2_pop, mb1_pop, mb2_pop -> mutated population
    """
    # Create a copy of all genes
    mw1_pop = deepcopy(w1_pop)
    mw2_pop = deepcopy(w2_pop)
    mb1_pop = deepcopy(b1_pop)
    mb2_pop = deepcopy(b2_pop)
    
    # Create uniformly distributed noise in shape of genes
    g1 = np.random.uniform(-1,1,(np.shape(w1_pop)))
    g2 = np.random.uniform(-1,1,(np.shape(w2_pop)))
    g3 = np.random.uniform(-1,1,(np.shape(b1_pop)))
    g4 = np.random.uniform(-1,1,(np.shape(b2_pop)))
    
    # 0 Noise for parents
    for i in indices:
        g1[i] = 0
        g2[i] = 0
        g3[i] = 0
        g4[i] = 0
    
    # Add noise "mutation" 
    mw1_pop = mw1_pop + g1*0.01
    mw2_pop = mw2_pop + g2*0.01
    mb1_pop = mb1_pop + g3*0.01
    mb2_pop = mb2_pop + g4*0.01
    
    return mw1_pop, mw2_pop, mb1_pop, mb2_pop

    
############################ Fitness Function #################################

def fitness_function(particles_cleared,sensor_distances,collision_count,timestep,v_l,v_r,fitness):
	global prev_v_r,prev_v_l,prev_fitness
	dist_threshold = 10
	terminate = False
	np_distances = np.asarray(sensor_distances)
	np_distances = np.where((np_distances > 10) & (np_distances < 40), 1, 0)
	closer_wall_factor = np.sum(np_distances)/12
	fitness += (4 * particles_cleared  + 10 * closer_wall_factor - 4 * collision_count) * (abs(v_l + v_r)/(60))
	if(timestep%30 == 0):
		prev_v_l = v_l
		prev_v_r = v_r
		prev_fitness = fitness
		if(prev_fitness < 0 and fitness < 0):
			terminate = True
		if(prev_v_l == 0 and prev_v_r == 0 and v_l == 0 and v_r == 0):
			terminate = True
	if(collision_count > 0 or int(v_l + v_r) == 0):
		terminate = True
	return fitness, terminate

	
###############################################################################