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

import matplotlib as mpl
import matplotlib.pyplot as plt
import time
from pygame.locals import *

# from sympy import * #Point, intersection
# from geometer.point import *
# from geometer.shapes import *
from copy import copy, deepcopy

pygame.init()

w_width = 800
w_height = 800
walls_thickness = 20

win = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('Simulator')

x = w_width / 2
y = w_height / 2

bot_c = Point(x, y)
angle = math.radians(0)  # Horizontal left is 0 degree. The degree increase anti-clockwise
radius = 20
length = 2 * radius
sens_l = 200  # 3*radius

nb_sensors = 12

v_l = 0
v_r = 0
run = True
w_pressed = False
s_pressed = False
tst = False  # Add sensor values text

no_paricles = 3000
radius_dust = 2
particles_cleared = 0
max_iters_pergen = 200
prev_v_r = 0
prev_v_l = 0
prev_fitness = 0
filename = time.strftime("%Y%m%d_%H%M%S", time.localtime())
################## Numbers ###################

n_gen = 5
n_pop = 10

##############################################

########### EA ##################
keep_n = 3
#################################

################# RGB Colors #################

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (13, 255, 0)
GREEN = Color("purple")
YELLOW = (255, 255, 0)
SENS_RED = (255, 0, 0)
BG_COLOR = Color("lightblue")


##############################################


################# Functions ##################

def fitness_function(particles_cleared, sensor_distances, collision_count, timestep, v_l, v_r, fitness):
    global prev_v_r, prev_v_l, prev_fitness
    dist_threshold = 10
    terminate = False
    np_distances = np.asarray(sensor_distances)
    np_distances = np.where((np_distances > 10) & (np_distances < 40), 1, 0)
    closer_wall_factor = np.sum(np_distances) / 12
    fitness += (4 * particles_cleared + 2 * closer_wall_factor - 4 * collision_count) * (abs(v_l + v_r) / (60))
    if (timestep % 30 == 0):
        prev_v_l = v_l
        prev_v_r = v_r
        prev_fitness = fitness
        if (prev_fitness < 0 and fitness < 0):
            terminate = True
        if (prev_v_l == 0 and prev_v_r == 0 and v_l == 0 and v_r == 0):
            terminate = True
    if (collision_count > 0 or int(v_l + v_r) == 0):
        terminate = True
    return fitness, terminate


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def CreateDust(no_paricles, width, height):
    np.random.seed(0) # The np.random.seed(0) in initialization doesn't help here. So this line is necessary
    random_coord = np.random.rand(no_paricles, 2)
    random_coord[:, 0] = random_coord[:, 0] * width
    random_coord[:, 1] = random_coord[:, 1] * height
    return random_coord


def CalculateDistance(dust_positions, center_bot):
    return np.array([distance(dust_position, center_bot) for dust_position in dust_positions])


def Clear_Dust(dust_positions, radius_dust, radius_circle, dust_distances):
    initial_dust_count = len(dust_positions)
    colliding_dust_indices = np.argwhere(dust_distances <= radius_dust + radius_circle)
    dust_positions = np.delete(dust_positions, colliding_dust_indices, 0)
    after_dust_count = len(dust_positions)
    return dust_positions, initial_dust_count - after_dust_count


def create_font(t,s=15,c=(0,0,0), b=False,i=False):
    font = pygame.font.SysFont("Arial", s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text

def plotting_errorbar(y):
    y_avg = np.mean(y, axis=1)
    std = np.std(y, axis=1)
    x = np.arange(0, len(y), 1)
    plt.errorbar(x, y_avg ,yerr=std,linestyle = '--', marker='x')
    plt.show()

def createWorld():
    return


def createBot():
    return


# dist_text = create_font(tt)


def ICC_Calculation2(v_r, v_l, radius, angle, x, y):
    #    global v_l, v_r, radius, angle, x, y
    if v_l != v_r:
        icc_distance = (radius) * (v_l + v_r) / (v_r - v_l)
        omega = (v_r - v_l) / (2 * radius)
        icc_x = x - (icc_distance * np.sin(angle))
        icc_y = y - (icc_distance * np.cos(angle))

        icc_x, icc_y = (x - icc_distance * np.sin(angle)), (y - icc_distance * np.cos(angle))

        a = np.matrix([[np.cos(omega), -np.sin(omega), 0],
                       [np.sin(omega), np.cos(omega), 0],
                       [0, 0, 1]])

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




def getPerpendicularPosition(point, line_start_point, line_end_point):
    x = np.array(point.coords[0])
    u = np.array(line_start_point.coords[0])
    v = np.array(line_end_point.coords[0])
    n = v - u
    n /= np.linalg.norm(n, 2)
    perpendicular_position = u + n * np.dot(x - u, n)
    return Point(perpendicular_position)


def collisionDetection(currect_center, center, radius, start_point, end_point):
    #### method from: https://stackoverflow.com/questions/39895330/2d-orthogonal-projection-of-vector-onto-line-with-numpy-yields-wrong-result
    perpendicular_position = getPerpendicularPosition(center, start_point, end_point)
    d = np.linalg.norm(np.array(center.coords[0]) - np.array(perpendicular_position.coords[0]))

    line = LineString([start_point, end_point])  # Check whether the perpendicular position is on the obstacle
    line2 = LineString(
        [currect_center, perpendicular_position])  # For checking whether the perpendicular position is on the obstacle.
    trajectory = LineString([currect_center, center])

    if d <= radius and line2.intersection(line).coords != []:
        # print('Colliding and d is {}'.format(d))
        return True
    elif trajectory.intersection(line).coords != []:  # Check backwords to avoiding clipping-through
        return True
    else:
        return False


def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def drawWalls():
    borders = [
        pygame.Rect(0, 0, w_width, walls_thickness),
        pygame.Rect(0, 0, walls_thickness, w_height),
        pygame.Rect(0, w_width - walls_thickness, w_width, walls_thickness),
        pygame.Rect(w_height - walls_thickness, 0, walls_thickness, w_height),
    ]

    for border in borders:
        pygame.draw.rect(win, BLACK, border)

    borders_line = [
        pygame.draw.line(win, RED, line_top.bounds[0:2], line_top.bounds[2:4], 2),
        pygame.draw.line(win, RED, line_right.bounds[0:2], line_right.bounds[2:4], 2),
        pygame.draw.line(win, RED, line_bottom.bounds[0:2], line_bottom.bounds[2:4], 2),
        pygame.draw.line(win, RED, line_left.bounds[0:2], line_left.bounds[2:4], 2),
        ]

    return borders, borders_line


def initilize_room(experiment_room):
    collision_room = [[0 for j in range(2)] for i in range(len(experiment_room.coords))]
    idx = 0
    for coord_x, coord_y in experiment_room.coords:
        # print(x, y)
        # print(idx)
        if idx == 0:
            collision_room[idx][0] = Point(coord_x, coord_y)
            collision_room[len(experiment_room.coords) - 1][1] = Point(coord_x, coord_y)
        elif 0 < idx <= len(experiment_room.coords) - 1:
            collision_room[idx - 1][1] = Point(coord_x, coord_y)
            collision_room[idx][0] = Point(coord_x, coord_y)
        else:
            pass
        idx += 1
    return collision_room


def drawRoom(collision_room):
    for i in range(len(collision_room)):
        pygame.draw.line(win, RED, (int(collision_room[i][0].x), int(collision_room[i][0].y)),
                         (int(collision_room[i][1].x), int(collision_room[i][1].y)), 2)


def collidingMovement(vr, vl, current_center, angle, start_point, end_point):
    velocity = (v_r + v_l) / 2
    center_after_v = Point(-np.cos(angle) * velocity + center.x,
                           np.sin(angle) * velocity + center.y)  # Moving straightford with angle velocity

    vector_obstacle = np.array(end_point.coords[0]) - np.array(start_point.coords[0])
    vector_trajectory = np.array(center_after_v.coords[0]) - np.array(center.coords[0])

    vector_obstacle_het = vector_obstacle / np.linalg.norm(vector_obstacle, 2)
    projection = np.dot(vector_trajectory, vector_obstacle) / np.linalg.norm(vector_obstacle) * vector_obstacle_het
    # print('projection is {}'.format(projection))
    new_position = np.array(current_center.coords[0]) + projection
    return new_position


def sensing(sensor, collision_walls, collision_room):
    detect = False
    dist = sens_l - radius
    inter_pt = None
    collision_sensing = collision_walls + collision_room

    for n in range(len(collision_sensing)):
        test = LineString([(int(collision_sensing[n][0].x), int(collision_sensing[n][0].y)),
                           (int(collision_sensing[n][1].x), int(collision_sensing[n][1].y))]).intersection(sensor)
        if not (test.is_empty):
            detect = True
            inter_pt = test
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])

    return detect, dist, inter_pt


def drawSensors():
    sensors_lines = []
    sensors = []
    distances = [None] * 12

    for i in range(nb_sensors):
        sensors_lines.append(LineString(
            [bot_c, (bot_c.x + sens_l * -np.cos(angle + np.radians((i * 360 / nb_sensors))),
                     (bot_c.y + sens_l * np.sin(angle + np.radians((i * 360 / nb_sensors)))))]
        )
        )
    for i in range(len(sensors_lines)):
        det, dist, int_pt = sensing(sensors_lines[i], collision_walls, collision_room)  # returns 3 values ('detection (bool)', 'distance (value)', 'Intersection point(Point)')
        distances[i] = dist
        #        print("Distance for sensor {}, = {}".format(i, dist))

        #### TODO TEXT HERE
        ###
        if det:
            sensors.append(
                #                    pygame.draw.line(win, GREEN, (int(x), int(y)), (x + sens_l * -np.cos(angle + np.radians(i * 360/nb_sensors)),
                #                                          (y + sens_l * np.sin(angle + np.radians(i * 360/nb_sensors))))),
                #                    )
                pygame.draw.line(win, Color("darkgreen"), (int(x), int(y)), (int_pt.x, int_pt.y), 2),
            )
            txt = create_font(str(round(dist, 0)))
            win.blit(txt, (int_pt.x, int_pt.y))

        else:
            sensors.append(
                pygame.draw.line(win, SENS_RED, (int(x), int(y)),
                                 (x + sens_l * -np.cos(angle + np.radians(i * 360 / nb_sensors)),
                                  (y + sens_l * np.sin(angle + np.radians(i * 360 / nb_sensors))))),
            )
            if not tst:
                txt = create_font(str(round(dist, 0)))
                win.blit(txt, (x + sens_l * -np.cos(angle + np.radians(i * 360 / nb_sensors)),
                               (y + sens_l * np.sin(angle + np.radians(i * 360 / nb_sensors)))))

    return distances


def drawspeeds():
    left_wheel_text = create_font(str(round(v_l)))
    win.blit(left_wheel_text, (x + radius * -np.cos(angle + np.pi / 2), (y + radius * np.sin(angle + np.pi / 2))))
    right_wheel_text = create_font(str(round(v_r)))
    win.blit(right_wheel_text, (x + radius * -np.cos(angle - np.pi / 2), (y + radius * np.sin(angle - np.pi / 2))))
    return ()

def save_weights_per_generation(filename, gen, mw1_pop, mw2_pop, mb1_pop, mb2_pop, fit_pop):
    f = open('weights{}'.format(filename), 'a')
    f.write('Generation : {}\n'.format(gen))
    f.write('nw1_pop : \n {}\n nw2_pop : \n {} \n mb1_pop : \n {} \n mb2_pop " \n {} \n fit_pop : \n {} \n'.format(
        mw1_pop, mw2_pop, mb1_pop, mb2_pop, fit_pop))
    f.close()

def save_weights_final_generation(filename, gen, mw1_pop, mw2_pop, mb1_pop, mb2_pop, fit_pop):
    f = open('weights{}'.format(filename), 'a')
    f.write('Generation : {}\n'.format(gen))
    f.write('nw1_pop : \n {}\n nw2_pop : \n {} \n mb1_pop : \n {} \n mb2_pop " \n {} \n fit_pop : \n {} \n'.format(
        mw1_pop, mw2_pop, mb1_pop, mb2_pop, fit_pop))
    f.close()
####################### NN ##########################
def initWeights():
    weight_l1 = np.random.randn(6, 12)
    weight_l2 = np.random.randn(2, 6)
    bias = np.random.randn()
    bias2 = np.random.randn()

    return weight_l1, weight_l2, bias, bias2


def feedForward(x, weight_l1, weight_l2, bias, bias2, r1, timestep):
    swap = False
    x = x.astype(np.float64)
    r1 = r1.astype(np.float64)
    if (timestep != 0 and timestep % 30 == 0):
        x[0:4] += r1[0:4]
    h1 = np.dot(weight_l1, x.T) + bias
    a1 = np.tanh(h1)
    if (timestep % 30 == 0):
        swap = True
        r1 = a1
    h2 = np.dot(weight_l2, a1.T) + bias2
    output = np.tanh(h2)
    return output, r1, swap


#####################################################
def Selection(w1_pop, b1_pop, w2_pop, b2_pop, fit_pop, best_size):
    indices = np.argpartition(fit_pop, -best_size)[-best_size:]
    w1_pop_elite = w1_pop[indices]
    b1_pop_elite = b1_pop[indices]
    w2_pop_elite = w2_pop[indices]
    b2_pop_elite = b2_pop[indices]
    return w1_pop_elite, b1_pop_elite, w2_pop_elite, b2_pop_elite


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


# Proportional selection -

# Rank-based selection -

# Tournament selection -


###############################################################################

################################ Replacement ##################################

def Reproduction(pop_size, elite_genes, best_size):
    offspring_count = int(pop_size / len(elite_genes))
    assert type(offspring_count) == int, "WTF are u doing"
    parent_genes = (np.tile(elite_genes, (offspring_count + 1, 1)))
    parent_genes = np.resize(parent_genes, (pop_size, 2))
    return parent_genes


###############################################################################

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
        new_indiv = [(w1_pop[father] + w1_pop[mother]) / 2]
        cw1 = np.concatenate((cw1, new_indiv))

    while (len(cw2) < len(w2_pop)):
        father, mother = np.random.choice(indices, 2, replace=False)
        new_indiv = [(w2_pop[father] + w2_pop[mother]) / 2]
        cw2 = np.concatenate((cw2, new_indiv))

    while (len(cb1) < len(b1_pop)):
        father, mother = np.random.choice(indices, 2, replace=False)
        new_indiv = [(b1_pop[father] + b1_pop[mother]) / 2]
        cb1 = np.concatenate((cb1, new_indiv))

    while (len(cb2) < len(b2_pop)):
        father, mother = np.random.choice(indices, 2, replace=False)
        new_indiv = [(b2_pop[father] + b2_pop[mother]) / 2]
        cb2 = np.concatenate((cb2, new_indiv))

    # Resize population to original size (since might be bigger than original)
    cw1 = np.resize(cw1, (np.shape(w1_pop)))
    cw2 = np.resize(cw2, (np.shape(w2_pop)))
    cb1 = np.resize(cb1, (np.shape(b1_pop)))
    cb2 = np.resize(cb2, (np.shape(b2_pop)))

    # Return population after crossover
    return cw1, cw2, cb1, cb2


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
    g1 = np.random.uniform(-1, 1, (np.shape(w1_pop)))
    g2 = np.random.uniform(-1, 1, (np.shape(w2_pop)))
    g3 = np.random.uniform(-1, 1, (np.shape(b1_pop)))
    g4 = np.random.uniform(-1, 1, (np.shape(b2_pop)))

    # 0 Noise for parents
    for i in indices:
        g1[i] = 0
        g2[i] = 0
        g3[i] = 0
        g4[i] = 0

    # Add noise "mutation"
    mw1_pop = mw1_pop + g1 * 0.01
    mw2_pop = mw2_pop + g2 * 0.01
    mb1_pop = mb1_pop + g3 * 0.01
    mb2_pop = mb2_pop + g4 * 0.01

    return mw1_pop, mw2_pop, mb1_pop, mb2_pop


###############################################################################

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

# start_point = Point(0, 2)  #### DEFINE THE LEFT MOST POINT AS END POINT
# end_point = Point(2, 2)  #### DEFINE THE RIGHT MOST POINT AS START POINT
# end_point = Point(0, 2)
# start_point = Point(2, 2)

line_top = LineString([b1_s, b1_e])
line_right = LineString([b2_s, b2_e])
line_bottom = LineString([b3_s, b3_e])
line_left = LineString([b4_s, b4_e])

#Room Initilization (vertices in order)
room1 = LineString([Point(200, 200), Point(200, w_width-200), Point(w_height-200, w_width-200), Point(w_height-200, 200)])
room2 = LineString([Point(100, 100), Point(400, 100), Point(w_height-100, 700), Point(300, 500)])
rooms = {'1' : room1, "2" : room2}

################# Define collison lines here #######################
collision_walls = [
        [b1_s, b1_e],
        [b2_s, b2_e],
        [b3_s, b3_e],
        [b4_s, b4_e]
        ]

# experiment_room = rooms[(input('Choose room1 (1) or room2 (2) -(default 1): \n>>') or '1')]
experiment_room = rooms['1']
collision_room = initilize_room(experiment_room)
####################################################################

# ################# INITIALIZATION ##################

borders, borders_line = drawWalls()
distances = drawSensors()
bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle),
                               (bot_c.y + radius * np.sin(angle)))])  # , int(radius/10))
# ###################################################

################### ------- MAIN LOOP ------- ######################
np.random.seed(0)
dust_positions = CreateDust(no_paricles, w_width - walls_thickness, w_height - walls_thickness)
timestep = 0
fitness = 0
w1_pop = np.random.randn(n_pop, 6, 12)
w2_pop = np.random.randn(n_pop, 2, 6)
b1_pop = np.random.randn(n_pop, 1)
b2_pop = np.random.randn(n_pop, 1)
recurrent1 = np.random.randn(6, 1)
fit_pop = np.empty((0, 1))
best_size = int(n_pop / 5)
# print("Weights: ", weights)
# print("weights0", weights[0])
print(fit_pop)

fitness_per_generation = []

while run:
    for gen in range(n_gen):
        print("Generation: ", gen)
        fit_pop = np.empty((0, 1))
        for pop in range(n_pop):
            x, y = (w_width / 2, w_height/2) #Reset coordinate for every population.
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
                distances = np.asarray(distances) / 180
                t_v, t_r_1, swap = feedForward(np.asarray(distances), w1, w2, b1, b2, recurrent1, t)
                if swap:
                    recurrent1 = t_r_1
                t_v_r, t_v_l = t_v
                v_r = t_v_r * 30
                v_l = t_v_l * 30

                if (v_r > 0):
                    v_r = np.min([v_r, 30])
                else:
                    v_r = np.max([v_r, -30])
                if (v_l > 0):
                    v_l = np.min([v_l, 30])
                else:
                    v_l = np.max([v_l, -30])

                ### Redraw
                win.fill((BG_COLOR))
                borders, borders_line = drawWalls()
                drawRoom(collision_room)

                #### Draw Dust
                distance_dust = CalculateDistance(dust_positions, (x, y))
                dust_positions, count_cleared = Clear_Dust(dust_positions, radius, radius_dust, distance_dust)
                particles_cleared += count_cleared
                for i in range(len(dust_positions)):
                    pygame.draw.circle(win, BLACK, (int(dust_positions[i, 0]), int(dust_positions[i, 1])), radius_dust)

                #### Collision stuff ######
                currect_center = Point(x, y)
                next_angle, next_x, next_y = ICC_Calculation2(v_r, v_l, radius, angle, x, y)
                center = Point(next_x, next_y)
                end_line = Point(next_x + radius * -np.cos(next_angle), y + radius * np.sin(next_angle))
                collision_count = 0
                absolute_velocity = (v_r + v_l) / 2
                colliding_walls = []

                # Detects walls and room
                for i in range(len(collision_walls)):
                    if (collisionDetection(currect_center, center, radius, collision_walls[i][0],
                                           collision_walls[i][1]) == True):
                        collision_count += 1
                        colliding_walls.append(collision_walls[i])

                for i in range(len(collision_room)):
                    if (collisionDetection(currect_center, center, radius, collision_room[i][0],
                                           collision_room[i][1]) == True):
                        collision_count += 1
                        colliding_walls.append(collision_room[i])

                # Movement
                if (collision_count == 0):
                    angle, x, y = next_angle, next_x, next_y
                    distances = drawSensors()
                    pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
                    bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle),
                                                   (bot_c.y + radius * np.sin(
                                                       angle)))])  # , int(radius/10))    pygame.draw.line(win, YELLOW, bot_line.bounds[0:2], bot_line.bounds[2:4], int(radius/10))         # surface to draw on, color, s_pt, e_pt, width
                    line = pygame.draw.line(win, YELLOW, (x, y),
                                            (x + radius * -np.cos(angle), (y + radius * np.sin(angle))),
                                            int(radius / 10))
                    drawspeeds()
                    bot_c = Point((x), (y))

                elif (collision_count == 1):
                    x, y = collidingMovement(v_r, v_l, currect_center, angle, colliding_walls[0][0],
                                             colliding_walls[0][1])
                    distances = drawSensors()
                    pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
                    bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle),
                                                   (bot_c.y + radius * np.sin(
                                                       angle)))])  # , int(radius/10))    pygame.draw.line(win, YELLOW, bot_line.bounds[0:2], bot_line.bounds[2:4], int(radius/10))         # surface to draw on, color, s_pt, e_pt, width
                    line = pygame.draw.line(win, YELLOW, (x, y),
                                            (x + radius * -np.cos(angle), (y + radius * np.sin(angle))),
                                            int(radius / 10))
                    drawspeeds()
                    bot_c = Point((x), (y))

                else:
                    distances = drawSensors()
                    pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
                    line = pygame.draw.line(win, YELLOW, (x, y),
                                            (x + radius * -np.cos(angle), (y + radius * np.sin(angle))),
                                            int(radius / 10))
                    drawspeeds()
                    #Movement when detecting two walls, to be investigated
                    v_r = -v_r
                    v_l = -v_l
                ###########################
                # Update / Call next tick #

                if angle > 2 * np.pi:
                    angle = angle - 2 * np.pi
                elif angle < -2 * np.pi:
                    angle = angle + 2 * np.pi
                timestep = timestep + 1
                fitness, terminate = fitness_function(count_cleared, distances, collision_count, timestep, v_l, v_r,
                                                      fitness)
                #    print(fitness)
                if (terminate):
                    break
                pygame.display.update()
            print(fitness)
            dust_positions = CreateDust(no_paricles, w_width - walls_thickness, w_height - walls_thickness)
            fit_pop = np.append(fit_pop, fitness)
            fitness = 0

        #### Selection ####
        print("Fitness pop array: ", fit_pop)
        e_w1, e_w2, e_b1, e_b2, e_indices = TruncSelect(n_pop, keep_n, fit_pop, w1_pop, w2_pop, b1_pop, b2_pop)
        #### Reproduction

        #### Crossover/Mutation
        cw1, cw2, cb1, cb2 = ariCrossover(w1_pop, w2_pop, b1_pop, b2_pop, e_w1, e_w2, e_b1, e_b2, e_indices)
        mw1_pop, mw2_pop, mb1_pop, mb2_pop = gausMutation(cw1, cw2, cb1, cb2, e_w1, e_w2, e_b1, e_b2, e_indices)
        w1_pop, w2_pop, b1_pop, b2_pop = mw1_pop, mw2_pop, mb1_pop, mb2_pop
        fitness_per_generation.append(fit_pop)

        # save_weights_per_generation(filename, gen, mw1_pop, mw2_pop, mb1_pop, mb2_pop, fit_pop)
    run = False

run = False
print("Fitpop", fit_pop)
###################################################
print("Cleared particles: {}".format(particles_cleared))

#### Plotting ####
plotting_errorbar(fitness_per_generation)


save_weights_final_generation(filename, gen, mw1_pop, mw2_pop, mb1_pop, mb2_pop, fit_pop)
pygame.quit()
