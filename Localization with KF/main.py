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
		win.fill((173, 216, 230)) # Refill to update screen
		maze.draw_borders(win)
		maze.draw_walls(win)
		maze.draw_beacons(win)
		sensor_model.initilize_sensors(bot_c, angle)
		cnt, detected_list, dist_list = sensor_model.draw_sensors(win, maze.beacons, bot_c, controller.radius, angle)
        
        ########## TODO :  Move into correct files
		if cnt > 2:
				print("{} Beacons detected, List: {}\nDist List: {}".format(cnt, detected_list, dist_list))
                
				C = (dist_list[0]**2-dist_list[1]**2 - detected_list[0][0]**2 + detected_list[1][0]**2 - detected_list[0][1]**2 + detected_list[1][1]**2)
				F = (dist_list[1]**2-dist_list[2]**2 - detected_list[1][0]**2 + detected_list[2][0]**2 - detected_list[1][1]**2 + detected_list[2][1]**2)
				A = (-2*detected_list[0][0] + 2*detected_list[1][0])
				B = (-2*detected_list[0][1] + 2*detected_list[1][1])
				D = (-2*detected_list[1][0] + 2*detected_list[2][0])
				E = (-2*detected_list[1][1] + 2*detected_list[2][1])
                
				new_x = ((C*E) - (F*B)) / ((E*A) - (B*D))
				new_y = 500 - (((C*D) - (A*F)) / ((B*D) - (A*E)))
				print("NEW X/Y = ", (new_x, new_y))
                
		print("Lenght of det list: {}\nLength of dist list: {}".format(len(detected_list), len(dist_list)))
        ## 2 eq. 2 Unknown:
        # x = CE - FB / EA - BD
        # y = CD - AF / BD - E
        

#        for i in range(len(detected_list)):
            
#        (x - x1)^2 + (y - y1)^2 = r^2_i
        
        
        #####################
        
        
		maze.update_screen(win, bot_c, angle=angle, radius=controller.radius)

		v, w = controller.update_speed()
		state = controller.update_pos()
		bot_c = Point(state[0], 500 -state[1])
		angle = state[2]



main()