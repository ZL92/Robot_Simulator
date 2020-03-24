# from motion_control import Motion
# from sensor import Sensor
from map import MapClass
# from track_pose import Pose
# from visualization import *
import pygame

def main():
	run = True
	game_map = MapClass()
	game_map.initilize_screen()
	game_map.draw_borders()
	game_map.draw_walls()
	# controller = Motion(game_map)
	while run:
		game_map.update_screen(x=50, y=50, angle=100, radius=20, deltaT=0)
		# v,w = controller.update_speed()
	run = False
main()