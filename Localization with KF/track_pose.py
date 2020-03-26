'''
Dealing with multiple features, use the average pose estimated over all features
Pose tracking with Kalman filter
'''
import numpy as np
class Pose(object):

	def __init__(self):
			pass
	def prediction(self,A,B,u,R,mu,cov):
		mu_bar = np.dot(A,mu) + np.dot(B,u)
		cov_bar = np.dot(np.dot(A,cov),A.T) + R
		return mu_bar,cov_bar