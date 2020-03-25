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
import maze
import pygame 
import numpy as np



class Motion(object):
    def __init__(self, bot_c, angle):
        self.coord_x = bot_c.x
        self.coord_y = bot_c.y
        self.angle = angle
        self.v = 0
        self.w = 0
        self.radius = 15
        self.deltaT = 2
        self.state = np.array([self.coord_x, self.coord_y, self.angle])

    def update_speed(self): # Checked
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ord("w"):
                    self.v += 0.1
                if event.key == ord("a"):
                    self.w -= 0.01
                if event.key == ord("s"):
                    self.v -= 0.1
                if event.key == ord("d"):
                    self.w += 0.01
                if event.key == ord("x"):
                    self.v = 0
                    self.w = 0
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.update_pos()
        # self.game_map.update_screen(self.state[0],self.state[1],self.state[2],self.radius,self.game_map.win,self.deltaT)
        return self.v, self.w

    def update_pos(self): # state[2] is correct. State[0] and [1] to be check
        self.movement_matrix = np.array([[self.deltaT * np.cos(self.state[2]), 0],
                                        [self.deltaT * np.sin(self.state[2]), 0],
                                         [0, self.deltaT]])
        self.movement_vector = np.array([self.v, self.w])
        self.state += np.dot(self.movement_matrix, self.movement_vector.T).T

        #print(state[2]) #state[2] is correct
        if self.state[2] > 2 * np.pi:
            self.state[2] = self.state[2] - 2 * np.pi
        elif self.state[2] < -2 * np.pi:
            self.state[2] = self.state[2] + 2 * np.pi
        # print(self.state)
        return self.state
