'''
Initilizing maze and point-based features
No walls, no collision with features
Known correspondence which means all features have unique labels

'''

class Map(object):
    map_width = 500
    map_height = 500

    def __init__(self):
        self.maze = []
        self.features = []

    def initilize_maze(self, maze_coordinates):
        #TODO
        return self.maze

    def initilize_features(self, feature_coordinates):
        # TODO
        return self.features