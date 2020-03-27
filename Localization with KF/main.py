from motion_control import Motion
from sensor import *
import maze
import pygame
import pygame.gfxdraw as pgfx
from shapely.geometry import *
from visualization import *
from track_pose import Pose
import numpy as np


def main():
	run = True
	predict_trail = []
	true_trail = []
	ellipse_trail = []
	pygame.init()
	win = pygame.display.set_mode((maze.map_width, maze.map_height))
	pygame.display.set_caption('Simulator')
	win.fill((173, 216, 230))
	bot_c = Point(50, 50)
	angle = np.pi*1.5
	controller = Motion(bot_c, angle)
	sensor_model = Sensor()
	correction = False
	A= np.identity(3)
	R = np.array([[0.2,0,0],[0,0.2,0],[0,0,0.2]])
	cov = np.array([[0.1,0,0],[0,0.1,0],[0,0,0.1]])
	mu = np.array([50,50,0])
	pose_tracker = Pose()

	while run:
		win.fill((173, 216, 230)) # Refill to update screen
		maze.draw_borders(win)
		maze.draw_walls(win)
		maze.draw_beacons(win)
		sensor_model.initilize_sensors(bot_c, angle)
		cnt, detected_list, dist_list, angle_list = sensor_model.draw_sensors(win, maze.beacons, bot_c, controller.radius, angle)
        
        ########## TODO :  Move into correct files
		if cnt > 2:
                
				C1 = (dist_list[0]**2-dist_list[1]**2 - detected_list[0][0]**2 + detected_list[1][0]**2 - detected_list[0][1]**2 + detected_list[1][1]**2)
				F1 = (dist_list[1]**2-dist_list[2]**2 - detected_list[1][0]**2 + detected_list[2][0]**2 - detected_list[1][1]**2 + detected_list[2][1]**2)
				A1 = (-2*detected_list[0][0] + 2*detected_list[1][0])
				B1 = (-2*detected_list[0][1] + 2*detected_list[1][1])
				D1 = (-2*detected_list[1][0] + 2*detected_list[2][0])
				E1 = (-2*detected_list[1][1] + 2*detected_list[2][1])
                
				new_x = ((C1*E1) - (F1*B1)) / ((E1*A1) - (B1*D1))
				new_y = 500 - (((C1*D1) - (A1*F1)) / ((B1*D1) - (A1*E1)))
				correction = True

        #####################


		v, w = controller.update_speed()
		state,B = controller.update_pos()
		u = np.array([v,w]).T
			#mu = state.T + np.random.normal(0,1,3).T
		i = 0
		mu_bar,cov_bar = pose_tracker.prediction(A,B,u,R,mu,cov)
		mu,cov = mu_bar,cov_bar
		if(correction):
			Z = np.array([new_x,new_y,state[2]])
			C = np.identity(3)
			Q = np.array([[0.01,0,0],[0,0.01,0],[0,0,0.01]])
			mu,cov = pose_tracker.correction(mu_bar,cov_bar,C,Q,Z.T)
		ellipse_state = [[mu[0], mu[1], cov[0,0], cov[1,1]]]
		ellipse_trail += ellipse_state

        

        
		while i < len(predict_trail)-1:
			maze.draw_predict_trail(win,i,predict_trail[i],predict_trail[i+1],3)
			i+=3
        
		for i in range(len(true_trail)-1):
			maze.draw_true_trail(win, i, true_trail[i], true_trail[i+1],2)
			i+=1
            
		bot_c = Point(state[0], 500 -state[1])

		angle = state[2]
		correction = False
#		print("Ellipses:", ellipse_trail)
		while i < len(ellipse_trail)-1:
			pgfx.ellipse(win, int(ellipse_trail[i][0]), int(500-ellipse_trail[i][1]), int(ellipse_trail[i][2]) , int(ellipse_trail[i][3]), (252, 157, 3))
			i+=1
            
		maze.update_screen(win, bot_c, angle=angle, radius=controller.radius)
        
		predicted_state = [[int(mu[0]),int(500-mu[1])]]
		predict_trail += predicted_state
		true_state = [[int(bot_c.x), int(bot_c.y)]]
		true_trail += true_state
#		print("cov :", cov)

main()
