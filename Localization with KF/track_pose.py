'''
Dealing with multiple features, use the average pose estimated over all features
Pose tracking with Kalman filter
'''
import numpy as np
class Pose(object):

	def __init__(self):
			pass
	def prediction(self,A,B,u,R,mu,cov):
		mu_bar = np.dot(A,mu) + np.dot(B,u) + np.random.normal(0,2,3)
		cov_bar = np.dot(np.dot(A,cov),A.T) + R
		return mu_bar,cov_bar

	def correction(self,mu_bar,cov_bar,C,Q,Z):
		inv_coeff = np.dot(np.dot(C,cov_bar),C.T) + Q
		try:
			inv = np.linalg.inv(inv_coeff)
		except np.linalg.LinAlgError:
			print("error")
			return mu_bar,cov_bar
		K = np.dot(np.dot(cov_bar,C.T),inv)
		mu = mu_bar + np.dot(K,Z - np.dot(C,mu_bar))
		cov = np.dot(np.identity(3) - np.dot(K,C),cov_bar)
		return mu,cov