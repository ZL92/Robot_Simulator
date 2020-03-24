import math


def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def sensing(maze, radius, sensors_line, bot_c):
    detect = False
    dist = self.sensor_range - radius
    inter_pt = None
    for i in len(maze):
        test = LineString([(int(maze[n][0].x), int(maze[n][0].y)),
                       (int(maze[n][1].x), int(maze[n][1].y))]).intersection(sensors_line)
        if not (test.is_empty):
            detect = True
            inter_pt = test
            dist = np.min([dist, (distance(bot_c.coords[0], inter_pt.coords[0]) - radius)])
    return detect, dist, inter_pt

