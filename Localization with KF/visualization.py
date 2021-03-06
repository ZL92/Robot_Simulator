'''
Ellipse: intermediate estimates of position and covariance
Solid line: actual robot trajectory
Dotted line: estimated robot trajectory
Feature: black point
Draw green line between robot and feature, if feature is in sensor range
'''


import pygame
import math
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pygame import Color
from pygame.math import Vector2
from shapely.geometry import *
from pygame.locals import *
from copy import copy, deepcopy

#############################
 #Visualization functions
#############################
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = Color("green")
YELLOW = (255, 255, 0)
SENS_RED = (255, 0, 0)
BG_COLOR = Color("lightblue")

def create_font(t,s=15,c=(0,0,0), b=False,i=False):
    font = pygame.font.SysFont("Arial", s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text




