# from motion_control import Motion
# from sensor import Sensor
import maze
# from track_pose import Pose
# from visualization import *
import pygame

def main():
	run = True
	pygame.init()
	win = pygame.display.set_mode((maze.map_width, maze.map_height))
	pygame.display.set_caption('Simulator')
	win.fill((173, 216, 230))
	# controller = Motion(game_map)
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		maze.draw_borders(win)
		maze.draw_walls(win)

		maze.update_screen(win, x=50, y=50, angle=100, radius=20)

	# 	# v,w = controller.update_speed()

main()