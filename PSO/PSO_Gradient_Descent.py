# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:43:21 2020
"""

import matplotlib.pyplot as plt 
import numpy as np
from matplotlib import cm
import seaborn as sns
import random
import decimal
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting 
from functions import Rosenbrock, dRosenbrock, Rastrigin, dRastrigin, Paraboloid, dParaboloid
import time
from tqdm import tqdm

class Gradient_Descent:
    
    def __init__ (self, F, dF, interval, nr_iteration, init_state, trueMin,hist):
        self.interval = interval
        self.F = F
        self.dF = dF
        self.nr_iteration = nr_iteration
        trueMin = trueMin
        state_gd = init_state
        
    
        learning_rate = 0.0002 # After experiment, 0.0002 works good.
#        state_gd = np.array([round(random.uniform(-interval,interval), 2),round(random.uniform(-interval,interval), 2)])
        #state_ga = [ 4.02656064 -2.254784  ]
       # nr_iteration=100
        gd_history=[]
        
        x = np.linspace(-interval,interval,50)
        y = np.linspace(-interval,interval,50)
        x, y = np.meshgrid(x, y)
#        try:
        z = np.array(F([x, y]))
        fig2 = plt.figure()
        ax = fig2.subplots()
        surf = ax.contourf(x, y, z, cmap=cm.plasma, alpha = 0.3)
        
        ax.set_xlim(-interval,interval)
        ax.set_ylim(-interval,interval)
#        plt.ion()
        plt.show()  
        plt.get_current_fig_manager().window.setGeometry(1000,400,600,600)


#            
        tmpPoints = ax.scatter((state_gd[:,0]), (state_gd[:,1]), s=50, c = 'white')
        if not hist: tmpPoints.remove()
        for i in tqdm(range(nr_iteration)):
            for j in range(len(state_gd)):
            #    state_gd = np.clip(state_gd ,-interval,interval)
#            f = (state_gd[0][0]**2 + 100 * (state_gd[0][1] - state_gd[0][0]**2)**2)
                f = F(state_gd[j])
                gd_history.append([state_gd[j],f])
                fi = np.array(dF(state_gd[j]))
                state_gd[j] = state_gd[j] - np.dot(learning_rate,fi)
                if i%1==0:
                    #print(state_gd[j])
                    tmpPoints = ax.scatter((state_gd[j][0]), (state_gd[j][1]), s=50, c='white')
            plt.pause(0.5)

            if not hist: tmpPoints.remove()


        tmpPoints = ax.scatter(trueMin[0], trueMin[1], facecolors='none', edgecolors='r', marker='D', s=50 )
        plt.pause(0.3)
        fig2.show()
#        plt.ioff()
        
        print("After {} tierations, the minimus is {} at {}".format(nr_iteration, gd_history[-1][1], gd_history[-1][0]))
#        except:
#            print("Derivative of {} not yet implemented!".format(F.__name__))
    