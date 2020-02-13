
import numpy as np
####Equations: https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/geometry/geo-tran.html###
def robot2global(x, y, x_translation, y_translation, theta):
    a = np.array([[np.cos(theta), -np.sin(theta), x_translation],
                   [np.sin(theta), np.cos(theta), y_translation],
                   [0, 0, 1]])
    b = np.array([[x],
                  [y],
                  [1]])
    c = np.dot(a, b)
    
    return c[0], c[1]

def global2robot(x, y, x_translation, y_translation, theta):
    a = np.array([[np.cos(theta), np.sin(theta), -x_translation * (np.cos(theta) + np.sin(theta))],
                   [-np.sin(theta), np.cos(theta), y_translation * (np.sin(theta) - np.cos(theta))],
                   [0, 0, 1]])
    b = np.array([[x],
                  [y],
                  [1]])
    c = np.dot(a, b)
    
    return c[0], c[1]

####In the rotation of coordinate system, anti-cloclwise means positive value; clockwise means negative value


#x_translation = 5
#y_translation = 4
#theta = 0 
#
#localx, localy = robot2global(0, 0, x_translation, y_translation,theta)
#a, b = global2robot(0, 0, x_translation, y_translation,theta)