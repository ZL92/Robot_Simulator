# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 16:08:17 2020

@author: arjun
"""

import numpy as np

def Rosenbrock(x,y):
    return (x**2 + 100 * (y - x**2)**2)

def Rastrigin(x,y):
#    return ((10 * 2) + (x**2 - 10 * np.cos(2 * np.pi * x) + y**2 - 10 * np.cos(2 * np.pi * x)))
    return ((10 * 2) + sum(x[i]**2 - 10 * np.cos(2 * np.pi * x[i]) for i in range(len(x))))

####Create Initial Population

def InitPopulation(pop_size):
    return 10*np.random.random((pop_size,2)) - 5

def TruncSelect(pop_size,best_size,eval_genes,genes):
    indices = np.argpartition(eval_genes, -best_size)[-best_size:]
    elite_genes = genes[indices]
    return elite_genes

def Reproduction(pop_size,elite_genes,best_size):
    offspring_count = int(pop_size/len(elite_genes))
    assert type(offspring_count) == int,"WTF are u doing"
    parent_genes = (np.tile(elite_genes,(offspring_count,1)))
    Crossover(parent_genes,pop_size,best_size)
    
def Crossover(parent_genes,pop_size,best_size):
    var = np.random.randint(0,2,(pop_size - best_size ,))
    var_zeros = np.zeros((best_size,))
    cross_chance = np.concatenate((var_zeros,var))
    for i in range(len(parent_genes)):
        if i > best_size - 1:
            
    print(cross_chance)
    
np.random.seed(0)
pop_size = 10
best_size = 2
genes = InitPopulation(pop_size)
out = Rosenbrock(genes[:,0],genes[:,1])
elite_genes = TruncSelect(pop_size = pop_size,best_size = best_size ,eval_genes= out,genes = genes)
Reproduction(pop_size,elite_genes,best_size)
