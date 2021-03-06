# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 16:08:17 2020
@author: arjun
"""

from functions import *
import numpy as np
from copy import deepcopy, copy
import matplotlib.pyplot as plt
from matplotlib import cm


# def Rosenbrock(x,y):
#    return (x**2 + 100 * (y - x**2)**2)
#
# def Rastrigin(x,y):
##    return ((10 * 2) + (x**2 - 10 * np.cos(2 * np.pi * x) + y**2 - 10 * np.cos(2 * np.pi * x)))
#    return ((10 * 2) + sum(x[i]**2 - 10 * np.cos(2 * np.pi * x[i]) for i in range(len(x))))

####Create Initial Population

def InitPopulation(pop_size):
    return 20 * np.random.random((pop_size, 2)) - 10


def TruncSelect(pop_size, best_size, eval_genes, genes):
    indices = np.argpartition(eval_genes, -best_size)[-best_size:]
    elite_genes = genes[indices]
    return elite_genes


def Reproduction(pop_size, elite_genes, best_size):
    offspring_count = int(pop_size / len(elite_genes))
    assert type(offspring_count) == int, "WTF are u doing"
    parent_genes = (np.tile(elite_genes, (offspring_count + 1, 1)))
    parent_genes = np.resize(parent_genes, (pop_size, 2))
    return parent_genes



def Crossover(parent_genes, pop_size, best_size, type_of_crossover):
    new_pop = deepcopy(parent_genes)

    if type_of_crossover == 0: #One-point
        the_point = np.random.randint(0, len(parent_genes),1)
        new_pop[the_point,1], new_pop[the_point,0] = new_pop[the_point,0], new_pop[the_point,1]
    if type_of_crossover == 1: #Uniform with ps = 0,5
        for i in range(len(new_pop)):
            if np.random.rand(1) < 0.5:
                new_pop[i, 1], new_pop[i, 0] = new_pop[i, 0], new_pop[i, 1]
            else:
                continue
            i+=1

    if type_of_crossover == 2: #Arithmetic
        weighting_factor = np.random.rand(1)
        for i in range(len(new_pop)):
            offspring1 = new_pop[i, 0] * weighting_factor + new_pop[i, 0] * (1 - weighting_factor)
            offspring2 = new_pop[i, 0] * (1 - weighting_factor) + new_pop[i, 0] * weighting_factor
            new_pop[i] = [offspring1, offspring2]

    return new_pop


def Mutation(parent_genes, best_size, pop_size):
    new_pop = deepcopy(parent_genes)  # Create deep copy of parentpool
    var_zeros = np.zeros((best_size))
    mut_chanceX = np.concatenate((var_zeros - 1, np.random.uniform(0, 1, (pop_size - best_size))))
    mut_chanceY = np.concatenate((var_zeros - 1, np.random.uniform(0, 1, (pop_size - best_size))))

    rng_mutationX = np.random.uniform(-1, 1, pop_size)  # 10 random uniform numbers
    rng_mutationY = np.random.uniform(-1, 1, pop_size)  # 10 random uniform numbers

    new_popX = np.where(mut_chanceX < mutation_prob, new_pop[:, 0], new_pop[:, 0] + rng_mutationX)
    new_popY = np.where(mut_chanceY < mutation_prob, new_pop[:, 1], new_pop[:, 1] + rng_mutationY)

    new_pop = np.array([new_popX, new_popY])

    return new_pop.T


functs = { '0' : Rosenbrock, '1' : Rastrigin}

F = functs[(input('Choose Rosenbrock (0) or Rastrigin (1) - (default 0)') or '0')]
print('Function: {}'.format(F))


np.random.seed(0)
pop_size = 200 
best_size = int(pop_size/10)
mutation_prob = 0.3
genes = InitPopulation(pop_size)
no_iterations = int(input('Number of iterations - (default 50)') or '50')

type_of_crossover = 2 # One-point (0), Uniform (1), Arithmetic(2)

print("###### Initial Generation######")
print(genes)
print("###############################")
############PLotting###############
interval = 5
x = np.linspace(-interval, interval, 50)
y = np.linspace(-interval, interval, 50)
x, y = np.meshgrid(x, y)
z = np.array(F([x, y]))



fig = plt.figure()
ax = fig.subplots()
surf =ax.contourf(x, y, z, cmap=cm.plasma, alpha = 1)
plt.ion()
plt.show()
ax.set_xlim(-interval, interval)
ax.set_ylim(-interval, interval)
clr = 'lime'



for generation in range(no_iterations):
    out = -F([genes[:, 0], genes[:, 1]])
    elite_genes = TruncSelect(pop_size=pop_size, best_size=best_size, eval_genes=out, genes=genes)
    parent_genes = Reproduction(pop_size, elite_genes, best_size)
    child_genes = Crossover(parent_genes, pop_size, best_size, type_of_crossover)
    new_genes = Mutation(child_genes, best_size, pop_size)
    print("######### Generation " + str(generation + 1) + " #########")
#    print(new_genes)
    print("<<< Current Gen. Pop. AVG Fitness::: \t", np.round(np.average(out),2))
    print("<<< Current Gen. Pop. BEST Fitness::: \t", np.round(np.abs(np.max(out)),2))
    print("<<< Current Gen. Pop. WORST Fitness::: \t", np.round(np.min(out),2))
    print("---------------------------------")
    genes = new_genes
    tmpPoints = ax.scatter((new_genes[:,0]), (new_genes[:,1]), s=15, c = clr)
    plt.pause(0.2)
    tmpPoints.remove()

tmpPoints = ax.scatter((new_genes[:,0]), (new_genes[:,1]), s=50, facecolors='aqua', edgecolors='aqua', marker='D', alpha = 0.7)
plt.show()
plt.pause(0.5)
plt.show()
plt.ioff()



# print(new_genes)
# print(new_genes-parent_genes)