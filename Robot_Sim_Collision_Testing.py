import pygame
import math
import numpy as np
from pygame.math import Vector2

pygame.init()


w_height = 800
w_width = 800
walls_thickness = 20

win = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('Simulator')

x = w_width/2
y = w_height/2
angle = math.radians(0)
radius = 20
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
    # print('Collision')
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
    if(dx == 0):
        slope2 = dy2/dx2
        if dy>=0:
            return np.pi/2 - math.atan(slope2)
        else:
            return -np.pi/2 - math.atan(slope2)
    if(dx2 == 0):
        slope1 = dy/dx
        if dy2>=0:
            return np.pi/2 - math.atan(slope1)
        else:
            return -np.pi/2 - math.atan(slope1)
    slope1 = dy/dx
    slope2 = dy2/dx2
    tan_angle = (slope1-slope2)/(1+slope1*slope2)
    return math.atan(tan_angle)    

        
#        (x - R(v_r, v_l, l) * np.sin(theta)), (y - R(v_r, v_l, l) * np.cos(theta))
        

        
################### Walls #######################

borders = [
    pygame.Rect(0, 0, w_width, walls_thickness), 
    pygame.Rect(0, 0, walls_thickness, w_height), 
    pygame.Rect(0, w_width-walls_thickness, w_width, walls_thickness), 
    pygame.Rect(w_height-walls_thickness, 0, walls_thickness, w_height), 
]


################################################### Define collison lines here
start_point = Vector2(350,350) #### DEFINE THE RIGHT MOST POINT AS START POINT
end_point = Vector2(150,350) #### DEFINE THE LEFT MOST POINT AS END POINT
start_point2 = Vector2(150,350)
end_point2 = Vector2(0,200)
# start_point = Vector2(0,700) #### DEFINE THE RIGHT MOST POINT AS START POINT
# end_point = Vector2(0,0) #### DEFINE THE LEFT MOST POINT AS END POINT
# start_point2 = Vector2(700,0)
# end_point2 = Vector2(0,0)
collison_walls = [[start_point,end_point],[start_point2,end_point2]]
###################################################
pygame.time.delay(60)
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
    next_angle,next_x,next_y = ICC_Calculation2(v_r, v_l, radius, angle, x, y)
    center = Vector2(next_x,next_y)
    end_line = Vector2(next_x + radius * -np.cos(next_angle),y + radius * np.sin(next_angle))
    collision_count = 0
    absolute_velocity = (v_r + v_l)/2
    colliding_walls = []
    for i in range(len(collison_walls)):
        if(Collision(center,radius,collison_walls[i][0],collison_walls[i][1]) == True):
            collision_count +=1
            colliding_walls.append(collison_walls[i])
    if(collision_count > 1):
        factor_x = 1
        factor_y = 1
        for i in range(len(colliding_walls)):
            suby = (colliding_walls[i][0].y - colliding_walls[i][1].y)
            subx = (colliding_walls[i][0].x - colliding_walls[i][1].x)
            if(subx != 0):
                line_angle = math.atan(suby/subx)
            else:
                line_angle = np.pi/2
            factor_x *= np.cos(line_angle)
            factor_y *= np.sin(line_angle)
        theta = Slope(colliding_walls[1][0],colliding_walls[1][1],colliding_walls[0][0],colliding_walls[0][1])
        x = x - absolute_velocity * factor_x * np.cos(theta) #* np.cos(angle)
        y = y + absolute_velocity * factor_y * np.sin(theta) #* np.cos(angle)
        pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
        line = pygame.draw.line(win, BLACK, (x, y), (x + radius * -np.cos(angle),(y + radius * np.sin(angle))))
    if(collision_count == 0):
        angle,x,y = next_angle,next_x,next_y
        pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
#    print("print: {}".format(x + radius * np.cos(angle)))
        line = pygame.draw.line(win, BLACK, (x, y), (x + radius * -np.cos(angle),(y + radius * np.sin(angle))))
    
        # angle, x, y = ICC_Calculation2(v_r, v_l, radius, angle, x, y)
    if(collision_count == 1):
        theta = Slope(colliding_walls[0][0],colliding_walls[0][1],center,end_line)
        if(theta == np.pi/2 or theta == -np.pi/2):
            pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
#    print("print: {}".format(x + radius * np.cos(angle)))
            line = pygame.draw.line(win, BLACK, (x, y), (x + radius * -np.cos(angle),(y + radius * np.sin(angle))))
        else:
            dy = colliding_walls[0][1].y - colliding_walls[0][0].y
            dx = colliding_walls[0][1].x - colliding_walls[0][0].x
            d1 = distance(colliding_walls[0][0],(x,y))
            d2 = distance(colliding_walls[0][0],(next_x,next_y))
            absolute_velocity = abs(absolute_velocity* np.cos(theta))
            if(dx!=0):
                direction = math.atan(dy/dx)
                an = x - absolute_velocity * np.cos(direction)
                bn = y - absolute_velocity * np.sin(direction)
                ap = x + absolute_velocity * np.cos(direction)
                bp = y + absolute_velocity * np.sin(direction)
                if(d1 - d2 > 0):
                    x = ap
                    y = bp
                else:
                    x = an
                    y = bn
            else:
                if(d1 - d2 > 0):
                    y = y + absolute_velocity 
                else:
                    y = y - absolute_velocity

            pygame.draw.circle(win, GREEN, (int(x), int(y)), radius)
            line = pygame.draw.line(win, BLACK, (x, y), (x + radius * -np.cos(angle),(y + radius * np.sin(angle)))) 
        if(colliding_walls[0][0] == (150,150)):
            print(ap,bp)
   
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
    collision_count = 0
    bent_line = pygame.draw.line(win,RED,start_point,end_point)
    bent_line2 = pygame.draw.line(win,RED,start_point2,end_point2)
    pygame.display.update()
pygame.quit()