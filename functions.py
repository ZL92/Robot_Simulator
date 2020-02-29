# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 19:51:19 2020
"""
import numpy as np


def Rosenbrock(x):
    return ((0 - x[0])**2 + 100 * (x[1] - x[0]**2)**2)

def dRosenbrock (x):
    dx = 2*x[0] - 400*x[0]*(x[1] - (x[0]**2))
    dy = 200*(x[1] - (x[0]**2))
    return dx, dy

def Rastrigin(x):
#    return ((10 * 2) + (x[0]**2 - 10 * np.cos(2 * np.pi * x[0]) + x[1]**2 - 10 * np.cos(2 * np.pi * x[1])))
    return ((10 * 2) + sum(x[i]**2 - 10 * np.cos(2 * np.pi * x[i]) for i in range(len(x))))

def dRastrigin(x):
    #d = sum(2 * (x[i] + 10 * np.pi * np.sin(2 * np.pi * x[i])) for i in range(len(x)))
    dx = 2 * (x[0] + 10 * np.pi * np.sin(2 * np.pi * x[0]))
    dy = 2 * (x[1] + 10 * np.pi * np.sin(2 * np.pi * x[1]))
    return dx, dy

def Paraboloid(x):
    return (x[0]**2/0.001) +(x[1]**2/0.001)

def dParaboloid(x):
    dx = 2000*x[0]
    dy = 2000*x[1]
    return dx, dy

def Easom(x):
    return (-np.cos(x[0]) * np.cos(x[1]) * np.exp(-((x[0] - np.pi)**2 + (x[1] - np.pi)**2)))

def dEasom(x):
    #TODO: Implement
    return 0

def Eggholder(x):
    return (-(x[1] + 47) * np.sin(np.sqrt(np.abs((x[0]/2) + (x[1] + 47)))) - x[0] * np.sin(np.sqrt(np.abs(x[0] - (x[1] + 47)))))

def dEggholder(x):
    #TODO: Implement
    return 0


########### TEST Vectorization ################3
def updatePbest(x, pbs, pbsl, F): 
    fitness_value = np.ones(20,)
    fitness_value = np.tile(F(x),int(len(pbs)/2))
    print(fitness_value)
    print("Shape: fitness_val: {}; pbs: {}, F: {}".format(np.shape(fitness_value), np.shape(pbs),np.shape(F(x))))
#    fitness_value *= F(x)
    print(fitness_value)
    print("Shape: Fx: {}; pbs: {}".format(fitness_value, pbs))
    pbest = np.min(F(x), pbs)
    pbestloc = np.argmin(x, pbsl)
    return pbest, pbestloc
    
def updateGbest(x):
    gbest = np.min(x)
    gbestloc = np.argmin(x)
    return gbest, gbestloc