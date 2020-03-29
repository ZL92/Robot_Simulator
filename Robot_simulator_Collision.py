import pygame
from pygame import Color
from pygame.math import Vector2
import math
import numpy as np
from shapely.geometry import *
from utils import *
#from sympy import * #Point, intersection
#from geometer.point import *
#from geometer.shapes import *

pygame.init()


w_width = 800
w_height = 800
walls_thickness = 20

win = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('Simulator')

x = w_height/2
y = w_height/2

bot_c = Point(x,y)
angle = math.radians(0) # Horizontal left is 0 degree.The degree increase anti-clock wise
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

def create_font(t,s=15,c=(0,0,0), b=False,i=False):
    font = pygame.font.SysFont("Arial", s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text
#dist_text = create_font(tt)


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
    perpendicular_position = getPerpendicularPosition(center, start_point, end_point)

    # d = np.linalg.norm(np.cross(np.asarray(start_point)-np.asarray(end_point), np.asarray(end_point)-np.asarray(center))) / np.linalg.norm(np.asarray(start_point)-np.asarray(end_point)) #Distance from center to obstacle
    d = np.linalg.norm(np.array(center.coords[0]) - np.array(perpendicular_position.coords[0]))

    line = LineString([start_point, end_point]) #Check whether the perpendicular position is on the obstacle
    line2 = LineString([currect_center, perpendicular_position]) # For checking whether the perpendicular position is on the obstacle.
    trajectory = LineString([currect_center, center])

    # if start_point == Point(550,900):
        # pygame.draw.line(win, YELLOW, np.array(perpendicular_position.coords[0]), np.array(currect_center.coords[0]))
        # print('d is {}\ncurrent_center is {}\ncenter is {} '.format(d, currect_center, center) )
        # print('d is {}'.format(d))

    if d <= radius and line2.intersection(line).coords !=[]:
        # print('Colliding and d is {}'.format(d))
        return True
    elif trajectory.intersection(line).coords != []: #Check backwords to avoiding clipping-through
        return True
    else:
        return False


def distance(p1,p2):	
    return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )	

    

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
        # pygame.draw.line(win, Color('orange'), test_line1.coords[0], test_line1.coords[1],4),
        # pygame.draw.line(win, Color('purple'), test_line2.coords[0], test_line2.coords[1],4),

        ]

    return borders, borders_line

def drawRoom(collision_room):
    for i in range(len(collision_room)):
        pygame.draw.line(win, RED, (int (collision_room[i][0].x), int (collision_room[i][0].y)),
                                    (int (collision_room[i][1].x), int (collision_room[i][1].y)), 2)



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

    #Initilize sensors_lines
    for i in range(nb_sensors):
        sensors_lines.append(LineString(
                                        [bot_c, (bot_c.x + sens_l * -np.cos(angle + np.radians((i * 360/nb_sensors))),
                                                 (bot_c.y + sens_l * np.sin(angle + np.radians((i * 360/nb_sensors)))))]
                                        )
                            )
    #Detection of each sensors_lines
    for i in range(len(sensors_lines)):
        det, dist, int_pt = sensing(sensors_lines[i], collision_walls, collision_room)
#        print("Distance for sensor {}, = {}".format(i, dist))
        
        #### TODO TEXT HERE
        ###
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

    return()

def drawspeeds():
    left_wheel_text = create_font(str(round(v_l)))
    win.blit(left_wheel_text, (x + radius * -np.cos(angle + np.pi/2),(y + radius * np.sin(angle + np.pi/2))))
    right_wheel_text = create_font(str(round(v_r)))
    win.blit(right_wheel_text, (x + radius * -np.cos(angle - np.pi/2), (y + radius * np.sin(angle - np.pi/2))))
    return()

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

start_point = Point(0, 500) #### DEFINE THE LEFT MOST POINT AS END POINT
end_point = Point(500, 500) #### DEFINE THE RIGHT MOST POINT AS START POINT
start_point2 = Point(550, 900)
end_point2 = Point(200, 200)

line_top = LineString([b1_s, b1_e])
line_right = LineString([b2_s, b2_e])
line_bottom = LineString([b3_s, b3_e])
line_left = LineString([b4_s, b4_e])

# test_line1 = LineString([start_point, end_point])
# test_line2 = LineString([start_point2, end_point2])


room1 = LineString([Point(200, 200), Point(200, w_width-200), Point(w_height-200, w_width-200), Point(w_height-200, 200)])
room2 = LineString([Point(100, 100), Point(400, 100), Point(w_height-100, 700), Point(300, 500)])
rooms = {'1':room1, "2": room2}

# ############## INITIALIZATION ####################
#
# borders, borders_line = drawWalls()
# drawSensors()
# bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle),
#                                           (bot_c.y + radius * np.sin(angle)))])
# ##################################################
            
            

################# Define collision lines here ##########################
collision_walls = [
        [b1_s, b1_e],
        [b2_s, b2_e],
        [b3_s, b3_e],
        [b4_s, b4_e],
        # [start_point, end_point],
        # [start_point2, end_point2]
        ]
# experiment_room = rooms[(input('Choose room1 (1) or room2 (2) -(default 1): \n>>') or '1')]
experiment_room = rooms['1']
collision_room = initilize_room(experiment_room)



####################################################################
########### ------- MAIN LOOP ------- #############

while run:
    pygame.time.delay(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 119:        # W-Key
                v_l += 2
            if event.key == 115:        # S-Key
                v_l -= 2
            if event.key == 111:        # O-Key
                v_r += 2
            if event.key == 108:        # L-Key
                v_r -= 2
            if event.key == 120:        # X-Key
                v_r = 0
                v_l = 0
            if event.key == 116:        # T-Key
                v_l += 2
                v_r += 2
            if event.key == 103:        # G-Key
                v_r -= 2
                v_l -= 2
            if event.key == 98:         # B-Key
                v_r = v_l = (v_r + v_l)/2
            if event.key == 113:
                if tst:
                    SENS_RED = (255, 0, 0)
                    tst = False
                else:
                    SENS_RED = BG_COLOR
                    tst = True
            
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
    drawRoom(collision_room)

    #### Collision stuff ######
    currect_center = Point(x, y)
    next_angle, next_x, next_y = ICC_Calculation2(v_r, v_l, radius, angle, x, y)
    center = Point(next_x,next_y)
    #end_line = Point(next_x + radius * -np.cos(next_angle), y + radius * np.sin(next_angle)) # What is this?
    collision_count = 0
    absolute_velocity = (v_r + v_l)/2
    colliding_walls = []
    for i in range(len(collision_walls)):
        if(collisionDetection(currect_center, center, radius, collision_walls[i][0], collision_walls[i][1]) == True):
            collision_count +=1	
            colliding_walls.append(collision_walls[i])
            # print('colliding at wall :', collision_walls[i][0], collision_walls[i][1])
            # print('##########')
    for i in range(len(collision_room)):
        if(collisionDetection(currect_center, center, radius, collision_room[i][0], collision_room[i][1]) == True):
            collision_count +=1
            colliding_walls.append(collision_room[i])

    if(collision_count == 0):	
        angle, x, y = next_angle, next_x, next_y
        # print("Angle: {}".format(np.degrees(angle)))
        drawSensors()
        pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
        bot_c = Point((x), (y))
        bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle), (bot_c.y + radius * np.sin(angle)))]) #, int(radius/10))    pygame.draw.line(win, YELLOW, bot_line.bounds[0:2], bot_line.bounds[2:4], int(radius/10))         # surface to draw on, color, s_pt, e_pt, width
        line = pygame.draw.line(win, YELLOW, (x, y), (x + radius * -np.cos(angle),(y + radius * np.sin(angle))), int(radius/10))
        drawspeeds()


    elif(collision_count == 1):
        x, y = collidingMovement(v_r, v_l, currect_center, angle, colliding_walls[0][0], colliding_walls[0][1])
        drawSensors()
        pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
        bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle),
                                       (bot_c.y + radius * np.sin(
                                           angle)))])  # , int(radius/10))    pygame.draw.line(win, YELLOW, bot_line.bounds[0:2], bot_line.bounds[2:4], int(radius/10))         # surface to draw on, color, s_pt, e_pt, width
        line = pygame.draw.line(win, YELLOW, (x, y), (x + radius * -np.cos(angle), (y + radius * np.sin(angle))),
                                int(radius / 10))
        drawspeeds()
        bot_c = Point((x), (y))

    else:
#        x = x
#        y = y
        drawSensors()
        pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
#        bot_line = LineString([bot_c, (bot_c.x + radius * -np.cos(angle),
#                                      (bot_c.y + radius * np.sin(angle)))]) #, int(radius/10))    pygame.draw.line(win, YELLOW, bot_line.bounds[0:2], bot_line.bounds[2:4], int(radius/10))         # surface to draw on, color, s_pt, e_pt, width
        line = pygame.draw.line(win, YELLOW, (x, y), (x + radius * -np.cos(angle),(y + radius * np.sin(angle))), int(radius/10))
        drawspeeds()
#        bot_c = Point((x), (y))
    ###########################
    # Update / Call next tick #

#    print("ANGLE = {}".format(angle))
    if angle > 2*np.pi : 
        angle = angle - 2*np.pi
    elif angle < -2*np.pi:
        angle = angle + 2*np.pi
#    print("Collisions: {}".format(collision_count))
    pygame.display.update()
###################################################
pygame.quit()