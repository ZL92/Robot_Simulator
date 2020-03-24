from motion_control import Motion
from sensor import *
import maze
import pygame
from shapely.geometry import *
from visualization import *

def main():
	run = True
	pygame.init()
	win = pygame.display.set_mode((maze.map_width, maze.map_height))
	pygame.display.set_caption('Simulator')
	win.fill((173, 216, 230))
	bot_c = Point(50, 50)
	angle = 0
	controller = Motion(bot_c, angle)
	sensor_model = Sensor()
	while run:
		win.fill((173, 216, 230))
		maze.draw_borders(win)
		maze.draw_walls(win)
		sensor_model.initilize_sensors(bot_c, angle)
		sensor_model.draw_sensors(win, maze.maze, bot_c, controller.radius, angle)

		maze.update_screen(win, bot_c, angle=angle, radius=controller.radius)

		v, w = controller.update_speed()
		state = controller.update_pos()
		bot_c = Point(state[0], state[1])
		angle = state[2]

	# 	# v,w = controller.update_speed()

main()