# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 16:08:17 2020

@author: arjun
"""

from functions import *

import numpy as np
from copy import deepcopy, copy

#def Rosenbrock(x,y):
#    return (x**2 + 100 * (y - x**2)**2)
#
#def Rastrigin(x,y):
##    return ((10 * 2) + (x**2 - 10 * np.cos(2 * np.pi * x) + y**2 - 10 * np.cos(2 * np.pi * x)))
#    return ((10 * 2) + sum(x[i]**2 - 10 * np.cos(2 * np.pi * x[i]) for i in range(len(x))))

####Create Initial Population

def InitPopulation(pop_size):
    return 10*np.random.random((pop_size,2)) - 5

def TruncSelect(pop_size,best_size,eval_genes,genes):
    indices = np.argpartition(eval_genes,-best_size)[-best_size:]
    elite_genes = genes[indices]
    return elite_genes

def Reproduction(pop_size,elite_genes,best_size):
    offspring_count = int(pop_size/len(elite_genes))
    assert type(offspring_count) == int,"WTF are u doing"
    parent_genes = (np.tile(elite_genes,(offspring_count+1,1)))
    parent_genes = np.resize(parent_genes, (10,2))
    return parent_genes
    
def Crossover(parent_genes,pop_size,best_size,type_of_crossover):
    ####type -0 for swapping x and y,-1 for addition and subtraction
    new_pop = deepcopy(parent_genes)
    for i in range(len(new_pop)):
        if i >= best_size:
            if i+1 < len(new_pop):
                if(type_of_crossover == 0):
                    p2y = new_pop[i+1,1]
                    p1y = new_pop[i,1]
                    new_pop[i,0] = new_pop[i+1,1]
                    new_pop[i+1,0] = new_pop[i,1]
                    new_pop[i,1] = p2y
                    new_pop[i+1,1] = p1y
                if(type_of_crossover == 1):
                    p1 = new_pop[i]
                    p2 = new_pop[i+1]
                    new_pop[i] = (p1 + p2)/2
                    new_pop[i] = (p1 - p2)/2
        i = i+1
    return new_pop

def Mutation(parent_genes, best_size):
    new_pop = deepcopy(parent_genes)                # Create deep copy of parentpool
    var_zeros = np.zeros((best_size))
    mut_chanceX = np.concatenate((var_zeros-1,np.random.uniform(0,1,(pop_size - best_size))))
    mut_chanceY = np.concatenate((var_zeros-1,np.random.uniform(0,1,(pop_size - best_size))))

    rng_mutationX = np.random.uniform(-1,1,10)       # 10 random uniform numbers
    rng_mutationY = np.random.uniform(-1,1,10)       # 10 random uniform numbers

    new_popX = np.where(mut_chanceX < mutation_prob, new_pop[:,0], new_pop[:,0]+rng_mutationX)
    new_popY = np.where(mut_chanceY < mutation_prob, new_pop[:,1], new_pop[:,1]+rng_mutationY)
    
    new_pop = np.array([new_popX, new_popY])

    return new_pop.T

np.random.seed(0)
pop_size = 10
best_size = 2
mutation_prob = 0.1
genes = InitPopulation(pop_size)
no_iterations = 40
print("###### Initial Generation######")
print(genes)
print("###############################")
for generation in range(no_iterations):
    out = -Rosenbrock([genes[:,0],genes[:,1]])
    elite_genes = TruncSelect(pop_size = pop_size,best_size = best_size ,eval_genes= out,genes = genes)
    parent_genes = Reproduction(pop_size,elite_genes,best_size)
    child_genes = Crossover(parent_genes,pop_size,best_size,1)
    new_genes = Mutation(child_genes, best_size)
    print("###### Generation " + str(generation+1)+"######")
    print(new_genes)
    print("#################################")
    genes = new_genes
#print(new_genes)
#print(new_genes-parent_genes)