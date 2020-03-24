'''
Dealing with multiple features, use the average pose estimated over all features
Pose tracking with Kalman filter
'''

class Pose(object):

	def __init__(self):
		self.position = []
		self.covariance = []
		self.actual_trajectory = []
		self.estimated_trajectory = []

	def sensing(self):

	def KF(self):
		pass
	def track_pose(self):
		pass
