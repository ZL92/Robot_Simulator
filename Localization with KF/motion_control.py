'''
Velocity-based motion model u = (v, w)
v-translation
w-rotation
Control robot with key board:
    W=increment 𝑣
    S=decrement 𝑣
    A=decrement 𝜔
    D=increment 𝜔
    X=stop
'''
import map as Map
import pygame 
import numpy as np

class Motion(object):
    def __init__(self,Map):
        self.coord_x = Map.map_width/2
        self.coord_y = Map.map_height/2
        self.angle = 0
        self.v = 0
        self.w = 0
        self.radius = 25
        self.game_map = Map
        self.deltaT = 30
        self.state = np.array([self.coord_x,self.coord_y,self.angle])

    def robot_control(self, keyboard_input):
        # TODO
        return self.coord_x, self.coord_y, self.angle

    def update_speed(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ord("w"):
                    self.v+=0.1
                if event.key == ord("a"):
                    self.w-=0.01
                if event.key == ord("s"):
                    self.v-=0.1
                if event.key == ord("d"):
                    self.w+=0.01
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.update_pos()
        self.game_map.update_screen(self.state[0],self.state[1],self.state[2],self.radius,self.game_map.win,self.deltaT)
        return self.v, self.w

    def update_pos(self):
        self.movement_vector = np.array([self.v,self.w*0.1])
        self.movement_matrix = np.array([[self.deltaT*np.cos(self.state[2]),0],
                                        [self.deltaT*np.sin(self.state[2]),0],
                                         [0,self.deltaT]])
        self.state+= np.dot(self.movement_matrix,self.movement_vector.T).T
        print(self.state)
        pass
