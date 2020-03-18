'''
Omnidirectional sensor for feature detection
Limited sensor range
Estimate distance and bearing(direction) of observed feature
'''

class Sensor(object):
    nr_sensors = 12
    sensor_range =180

    def __init__(self):
        self.sensor_distance = []
        self.sensor_bearing = []

    def sensing(selfs, maze, features):
        # TODO
        return self.sensor_distance, self.sensor_bearing

