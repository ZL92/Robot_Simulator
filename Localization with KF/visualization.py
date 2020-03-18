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
from utils import *
from pygame.locals import *
from copy import copy, deepcopy

#############################
 #Visualization functions
#############################

def create_font(t,s=15,c=(0,0,0), b=False,i=False):
    font = pygame.font.SysFont("Arial", s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text

def draw_robot():
    #TODO

def draw_maze():
    #TODO

def draw_features():
    #TODO

def draw_sensors():
    # TODO

def draw_speed():
    #TODO

def draw_trajectory():
    #TODO



