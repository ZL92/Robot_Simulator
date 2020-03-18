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

class Motion(object):
    def __init__(self):
        self.coord_x = 100
        self.coord_y = 100
        self.angle = 0
        self.v = 0
        self.w = 0
        self.radius = 10

    def robot_control(self, keyboard_input):
        # TODO
        return self.coord_x, self.coord_y, self.angle

    def update_speed(self):
        # TODO
        return self.v, self.w
