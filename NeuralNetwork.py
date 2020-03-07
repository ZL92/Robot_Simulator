# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 15:57:15 2019

@author: ammar
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time

class NeuralNetwork():
    def __init__(self, hid_size):#, x, y):   
        np.random.seed(8)                
        self.alpha = 0.125
        self.lbda = 0.0001
        
        self.syn_w1 = np.random.rand(x.shape[0]+1,hid_size)
        self.syn_w2 = np.random.rand(hid_size,y.shape[0])
        print("syn 1: {}\nsyn 2: {}".format(self.syn_w1, self.syn_w2))
        
        self.x_bias = np.array(np.ones((8,1)))
        self.hid_bias = np.array(np.ones((8,1)))
        
        self.lossArray = []
        self.timeArray = []
        self.iterArray = []
        self.w1Array = np.array([])
        #self.w2Array = np.array([[]])
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sig_derivative(self, x):
        return (x * (1 - x))
    
    def tanh(x):
        t = (np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x))
        dt = 1 - t**2
        return t, dt
       
    """
    x : matrix of trianing inputs
    y : matrix of expected outputs
    """
    def training(self, x, y, epochs):
        init_time=time.time()
        print("Train during",epochs, "epochs.")
        for it in range(epochs):
            #todo
            self.feedforward(x)
            self.backprop(x, y)
            #print(self.compute_loss_function(y, self.output))
            self.lossArray.append(self.compute_loss_function(y, self.output))
            self.timeArray.append(time.time()-init_time)
            self.iterArray.append(it)
            #np.concatenate((self.w1Array, self.syn_w1[:,1]))
            #np.concatenate((self.w2Array, self.syn_w2))
            #print(output)
        print("Finished training in:",str(round((time.time()-init_time),3)),"seconds")
        
    
    def feedforward(self, x):
        self.hid = self.sigmoid(np.dot(x, self.syn_w1))
        self.hid[:,0] = 1
        #print(self.hid)
        self.output = self.sigmoid(np.dot(self.hid, self.syn_w2))
        print(self.output)
            
    def backprop(self, x, y):
        #Start calculating error:
        self.output_error = self.output - y
        #self.output_error = (self.output - y)* self.sig_derivative(self.output)
        self.delta_w2 = np.dot(self.hid.T, self.output_error) + self.lbda
        
        self.hid_error = self.sig_derivative(self.hid).T * ((np.dot(self.syn_w2, self.output_error)))
        self.delta_w1 = np.dot(x.T, self.hid_error.T) + self.lbda
        
        self.syn_w1 -= self.alpha * self.delta_w1
        self.syn_w2 -= self.alpha * self.delta_w2
        #hid_error = self.sig_derivative()
        
        
    def compute(self, inputs):
        self.hid = self.sigmoid(np.dot(inputs, self.syn_w1))
        #print(self.hid)
        self.hid[:,0] = 1
        print("Hidden Layer activation = ")
        print(" ~~~~~~> ", np.around(self.hid,2))
        self.output = self.sigmoid(np.dot(self.hid, self.syn_w2))
        print("Output after training on input:")
        print(self.output)
        #print(self.output)
        print(np.argmax(self.output)+1)
        
    def compute_loss_function(self, y, output):
        return -np.average(np.sum(y * np.log(output) + (1-y)*np.log(1-output)))
    
if __name__ == "__main__":
    # Training Inputs --> 'x'
    x = np.identity(8, dtype = int)
    x_bias = np.array(np.ones((8,1),dtype = int))
    y = np.copy(x)
    x = np.concatenate((x_bias,x),axis = 1)

    #hid = np.array([[1],[0],[0],[0]])    
    #hid_bias = np.array(np.ones((1,1),dtype = int))
    
    #x_w_bias = np.concatenate((x_bias, x), axis=1)
    print("X:" )
    print(x)

    #Init Neural Network
    neural_network = NeuralNetwork(4)

    #hid_w_bias = np.concatenate((hid_bias, hid), axis=1)
    print("W1:" )
    print(neural_network.syn_w1)
    print("W2:" )
    print(neural_network.syn_w2)
    
    neural_network.training(x, y, 2000)
    
    """
    timeArr = []
    itArr = []
    o1Arr = []
    o2Arr = []
    o3Arr = []
    o4Arr = []
    o5Arr = []
    o6Arr = []
    o7Arr = []
    o8Arr = []
    for it in range(50):
        timeSave = time.time()
        neural_network.training(x,y, 1000*it)
        timeArr.append(time.time()-timeSave)
        
        itArr.append(it)
        o1Arr.append(neural_network.output[0])
        o2Arr.append(neural_network.output[1])
        o3Arr.append(neural_network.output[2])
        o4Arr.append(neural_network.output[3])
        o5Arr.append(neural_network.output[4])
        o6Arr.append(neural_network.output[5])
        o7Arr.append(neural_network.output[6])
        o8Arr.append(neural_network.output[7])
        """
    
    test1 = np.array([[1,1,0,0,0,0,0,0,0]])
    test2 = np.array([[1,0,1,0,0,0,0,0,0]])
    test3 = np.array([[1,0,0,1,0,0,0,0,0]])
    test4 = np.array([[1,0,0,0,1,0,0,0,0]])
    test5 = np.array([[1,0,0,0,0,1,0,0,0]])
    test6 = np.array([[1,0,0,0,0,0,1,0,0]])
    test7 = np.array([[1,0,0,0,0,0,0,1,0]])
    test8 = np.array([[1,0,0,0,0,0,0,0,1]])
    print("Test: Expect max @ 1")
    neural_network.compute(test1)
    print("Test: Expect max @ 2")
    neural_network.compute(test2)
    print("Test: Expect max @ 3")
    neural_network.compute(test3)
    print("Test: Expect max @ 4")
    neural_network.compute(test4)
    print("Test: Expect max @ 5")
    neural_network.compute(test5)
    print("Test: Expect max @ 6")
    neural_network.compute(test6)
    print("Test: Expect max @ 7")
    neural_network.compute(test7)
    print("Test: Expect max @ 8")
    neural_network.compute(test8)
    
    print("Loss over Time")
    plt.plot(neural_network.iterArray, neural_network.lossArray)
    
    plt.figure()
    print("Iterations over Time")
    plt.plot(neural_network.iterArray, neural_network.timeArray)