# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 19:07:14 2020

@author: ammar
"""

import numpy as np

def velocity(v_r, v_l):
    return (v_r + v_l)/2

def angular_rotation(v_r, v_l, l):
    #v_r: Velocity Right
    #v_l: Velocity Left
    #l : distance between middle of wheels
    return (v_r - v_l)/l

def R(v_r, v_l, l):
    return ((l/2) * ((v_r + v_l)/(v_r - v_l)))

def ICC(x, y, v_r, v_l, l):
    
    ## TODO: theta
    return (x - R(v_r, v_l, l) * np.sin(theta)), (y - R(v_r, v_l, l) * np.cos(theta))