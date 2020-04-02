import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import cm
import seaborn as sns
import random
import decimal
import copy

def Rosenbrock(x):
    output = pow(x[0],2) + pow(x[1] - pow(x[0],2),2)
    return output

random.seed(0)
no_particles = 20
no_dimensions = 2
max_iters = 1000

interval=10


a = 2
b = 2
w1 = 0.9
w2 = 0.4

state = np.zeros((no_particles,no_dimensions))
velocity = np.zeros((no_particles,no_dimensions))
particle_best_score = np.ones(no_particles)* 1000
particle_best_location = np.zeros((no_particles,no_dimensions))

global_best = 1000

#plotting
def Rosenbrock_plt(x, y):
    output = pow(x,2) + pow(y - pow(x,2),2)
    return output

x = np.linspace(-interval,interval,num = no_particles)
y = np.linspace(-interval,interval,num = no_particles)
x, y = np.meshgrid(x, y)
z = Rosenbrock_plt(x, y)

for i in range (no_particles):
    for d in range (no_dimensions):
        state[i][d] = float(decimal.Decimal(random.randrange(-500, 500))/100)
        velocity[i][d] = float(decimal.Decimal(random.randrange(-200, 200))/100)

fig = plt.figure()
ax = fig.gca(projection='3d')        
surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm)
for k in range(max_iters):
    for i in range (no_particles):
        fitness_value = Rosenbrock(state[i])
        if fitness_value < particle_best_score[i]:
            particle_best_score[i] = fitness_value
            particle_best_location[i] = state[i]
        if fitness_value < global_best:
            global_best = fitness_value
            global_best_location = state[i]
        if k%100 == 0:
            ax.scatter(state[i][0], state[i][1], zs=Rosenbrock(state[i]), zdir='y', c='green')
            print(state[i])
        w = ((w1 - w2)*(max_iters -k)/max_iters) + w2
        velocity[i] = (w * velocity[i]) + (a * random.uniform(0,1) * (particle_best_location[i] - state[i]))+ (b * random.uniform(0,1) * (global_best_location - state[i]))
        state[i] = state[i] + velocity[i]
        

ax.view_init(elev=30., azim=35)
plt.show()
################################################
#x = np.linspace(-interval,interval,num = no_particles)
#y = copy.copy(x)
#xmesh, ymesh = np.meshgrid(x, y) #x = y.transpose()
#
#c = np.dstack((xmesh,ymesh)
#
#for i in range(no_particles):
#    for j in range(no_particles):
#        z[i][j]=Rosenbrock(c[i][j])
#fig = plt.figure()
#ax = fig.gca(projection='3d')
#
#surf = ax.plot_surface(xmesh, ymesh, z, cmap=cm.coolwarm)
#plt.show()
#################################################




#fig = plt.figure()
#ax = fig.gca(projection='3d')
#
#surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm)
#ax.scatter(particle_best_location[0][0], particle_best_location[0][1], zs=Rosenbrock(particle_best_location[0]), zdir='y', c='green')
#ax.view_init(elev=-90., azim=-35)
#plt.show()