# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 19:55:15 2020
"""
#### Imports Libraries ####
from matplotlib import cm, ticker
import matplotlib.pyplot as plt 
import matplotlib.colors as colors
from matplotlib.colors import ListedColormap, LogNorm
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting 
import seaborn as sns
import numpy as np
import random
import decimal
from functions import Rosenbrock, dRosenbrock, Rastrigin, dRastrigin, Paraboloid, dParaboloid, Easom, Eggholder, dParaboloid
import time
from PSO_Gradient_Descent import Gradient_Descent
from tqdm import tqdm



matplotlib_axes_logger.setLevel('ERROR') ## To supress Warning related to color

#### Define functions from functions.py #####
functs = {
   # 'Gradient' : Gradient_Descent,
    '0' : (Paraboloid, dParaboloid),
    '1' : (Rastrigin, dRastrigin),
    '2' : (Rosenbrock, dRosenbrock),
    '3' : (Easom, 0),
    '4' : (Eggholder, 0)
}



######### Settings params
#### Ask User for input ####
print("Press [Enter] for default option".format())
no_particles = int(input("Number of particles - (default 20): \n>>") or 20) #20
max_iters = int(input("Number of iterations - (default 100): \n>>") or 100) #1000
F, dF = functs[(input('Chose Paraboloid (0), Rastrigin (1), Rosenbrock (2), Easom (3) or Eggholder (4) - (default 0): \n>>') or '0')]

print("F: {}\ndF: {}".format(F,dF))

gd = False
xdim = False
hist = False

trueMin = [0,0]
if F.__name__ == 'Eggholder':
    interval = 600
    trueMin = [512, 404.2319]
elif F.__name__ == 'Easom':
    interval = int(input("Size of interval - (default 5): \n>>") or 5) #1000
    trueMin = [np.pi, np.pi]
else:
    interval = int(input("Size of interval - (default 5): \n>>") or 5) #1000
xdim = bool(int(input("3D plots? Yes (1) or No (0) (W: might be slow) (default 0): \n>>") or 0))

if not (xdim):
    gd = bool(int(input('Compare to Gradient Descent? Yes (1), No (0)? - (default 0): \n>>') or 0))
    
hist = bool(int(input("Keep History ? Yes(1) / No(0) (default 0): \n>>") or 0))


#
## Construct the colormap
#current_palette = sns.color_palette("bright")
#cmap = ListedColormap(sns.color_palette(current_palette).as_hex())

random.seed(0)
no_dimensions = 2
a = 2
b = 2
w1 = 0.9
w2 = 0.4


#### Initialize states, velocities, pbest, gbest, plot functionspace
state = np.zeros((no_particles,no_dimensions))
velocity = np.zeros((no_particles,no_dimensions))
particle_best_score = np.ones(no_particles)
particle_best_location = np.zeros((no_particles,no_dimensions))

x = np.linspace(-interval,interval,50)
y = np.linspace(-interval,interval,50)
x, y = np.meshgrid(x, y)

z = np.array(F([x, y]))
for i in range (no_particles):
    for d in range (no_dimensions):
        state[i][d] = round(random.uniform(-interval,interval), 2)
        velocity[i][d] = round(random.uniform(-20,20), 2)
    particle_best_score[i] = F(state[i])
    particle_best_location[i] = state[i]

init_state = state

global_best = np.min(F(state[:].T))
global_best_location = state[np.argmin(F(state[:].T))]

fig = plt.figure()  
if xdim:
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.plasma, alpha = 0.1)
else:
    ax = fig.subplots()
    surf = ax.contourf(x, y, z, cmap=cm.plasma, alpha = 1)
plt.ion()
plt.show()  
plt.get_current_fig_manager().window.setGeometry(300,400,600,600)
ax.set_xlim(-interval,interval)
ax.set_ylim(-interval,interval)


#### PSO ####
##### 3-D visualization ######
if xdim:
    tmpPoints = ax.scatter((state[:,0]), (state[:,1]), zs=F(state[:].T)+10, zdir='z', s=15, c = 'lime')
else:
    tmpPoints = ax.scatter((state[:,0]), (state[:,1]), s=15, c = 'lime')
plt.pause(1)
if not hist: tmpPoints.remove()
clr = 'lime'
for k in tqdm(range(max_iters)):
    if hist : clr = ([(k*(1/max_iters)),0,0])#(k*(1/max_iters)),(k*(1/max_iters))])
#    clr = ([(k*(1/max_iters)),(k*(1/max_iters)),(k*(1/max_iters))]) if hist == True else 'white'
    for i in range (no_particles):
        fitness_value = F(state[i])

        if fitness_value < particle_best_score[i]:
            particle_best_score[i] = fitness_value
            particle_best_location[i] = state[i]
        
        if fitness_value < global_best:
            global_best = fitness_value
            global_best_location = state[i]
    w = ((w1 - w2)*(max_iters -k-1)/max_iters) + w2
    velocity = np.clip((w * velocity) + (a * random.uniform(0,1) * (particle_best_location - state)) + (b * random.uniform(0,1) * (global_best_location - state)),-2,2)
    state = np.clip((state + velocity),-interval,interval)
    if xdim:
#        if (hist and ((k==0) or (k+1==max_iters) or (k==int((max_iters-1)/2)))):
        tmpPoints = ax.scatter((state[:,0]), (state[:,1]), zs=F(state[:].T), zdir='z', s=15, c = clr)#, c = clr)#c='white')
    else:
        tmpPoints = ax.scatter((state[:,0]), (state[:,1]), s=15, c = clr)#c='white')
    plt.pause(0.15)
    if not hist: tmpPoints.remove()
if xdim:    #3d
    print("True Min NYI in 3D")
    tmpPoints = ax.scatter((state[:,0]), (state[:,1]), zs=F(state[:].T), zdir='z', s=50, facecolors='aqua', edgecolors='aqua', marker='D', alpha = 0.7)
    tmpPoints = ax.scatter(trueMin[0], trueMin[1], zs=F((trueMin[0], trueMin[1],)), zdir='z', s=75, facecolors='red', edgecolors='yellow', marker='o', alpha = 1)
    plt.show()
    plt.pause(0.3)

#    ax.scatter(trueMin[0], trueMin[1], zs=F(trueMin), c='black')
else:       #2d
    tmpPoints = ax.scatter((state[:,0]), (state[:,1]), s=50, facecolors='aqua', edgecolors='aqua', marker='D', alpha = 0.7)
    tmpPoints = ax.scatter(trueMin[0], trueMin[1], facecolors='red', edgecolors='yellow', marker='o', s = 100)
    plt.show()
    plt.pause(0.3)

#### End
print("Fit val:{}".format(fitness_value))
#print("PBest: \n{}".format(particle_best_location)) #particle_best_location[0])
#print('Rounded PBest: \n{}'.format(np.round(particle_best_location)))
plt.show()
plt.ioff()

if gd:
    print("Comparing to gradient descent")
    Gradient_Descent(F,dF,interval, max_iters, init_state, trueMin, hist)

print("<<<<<<<<<<<< END >>>>>>>>>>")
