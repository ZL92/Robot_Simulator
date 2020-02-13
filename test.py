import pygame
import math
import numpy as np
pygame.init()

win = pygame.display.set_mode((800,800))
pygame.display.set_caption('Simulator')

x=400
y=400
angle =0
radius = 25
velocity_l = 0
velocity_r = 0
run = True
w_pressed = False
s_pressed = False

def ICC_Calculation():
	global velocity_l,velocity_r,radius,angle,x,y
	if velocity_l - velocity_r != 0:
		icc_distance = (radius)*(velocity_r + velocity_l)/(velocity_r - velocity_l)
		omega = (velocity_r - velocity_l)/(2*radius)
		icc_x = x - (icc_distance * math.sin(angle))
		icc_y = y - (icc_distance * math.cos(angle))
		a = np.matrix([[math.cos(omega),-math.sin(omega),0],[math.sin(omega),math.cos(omega),0],[0,0,1]])
		b = np.array([x - icc_x,y - icc_y, angle]).T
		c = np.array([icc_x,icc_y, omega]).T
		output_vector = np.dot(a,b) + c
		x = output_vector[0,0]
		y = output_vector[0,1]
		angle = output_vector[0,2]
	if velocity_l == velocity_r:
		x = x + velocity_r * math.cos(angle)
		y = y + velocity_r * math.sin(angle)

while run:
	pygame.time.delay(100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			#print(event.key)
			if event.key == 119:
				velocity_l+=1
			if event.key == 115:
				velocity_l -=1
			if event.key == 111:
				velocity_r+=1
			if event.key == 108:
				velocity_r-=1
			if event.key == 120:
				velocity_r =0
				velocity_l =0
			if event.key == 111:
				velocity_l+=1
				velocity_r+=1
			if event.key == 103:
				velocity_r-=1
				velocity_l-=1
	win.fill((0,0,0))
	# oldx = x
	# oldy = y
	ICC_Calculation()
	# if((x<25 or x>775)):
	# 	print('x border')
	# 	pygame.draw.circle(win,(255,255,255),(int(oldx),int(y)),radius)
	# elif((y<25 or y>775)):
	# 	print('Y border')
	# 	pygame.draw.circle(win,(255,255,255),(int(x),int(oldy)),radius)
	# else:
	pygame.draw.circle(win,(255,255,255),(int(x),int(y)),radius)
	pygame.draw.line(win,(0,0,0),(x,y),(x+radius*math.cos(angle),y+radius*math.sin(angle)))
	pygame.display.update()
pygame.quit()