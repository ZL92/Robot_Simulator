from motion_control import Motion
from sensor import Sensor
from map import Map
from track_pose import Pose
from visualization import *

def main():
	run = True
	game_map = Map(800,800)
	controller = Motion(game_map)
	while run:
		v,w = controller.update_speed()
	run = False
main()