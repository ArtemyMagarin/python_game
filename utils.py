def get_nearest_point(point, points):
    s = list(map(lambda p: calculate_distance(point, p), points))
    return points[s.index(min(s))]


def calculate_velocity(point_from, point_to, speed):
    distance = calculate_distance(point_from, point_to)   
    velocity_x = (point_to[0] - point_from[0]) * speed / distance
    velocity_y = (point_to[1] - point_from[1]) * speed / distance
    return (velocity_x, velocity_y)


def calculate_distance(point_from, point_to):
    base_x = point_to[0] - point_from[0]
    base_y = point_to[1] - point_from[1]
    distance = pow(pow(base_x, 2) + pow(base_y, 2), 0.5) 
    return distance
