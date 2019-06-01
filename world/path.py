import heapq
from world.world import KutuluWorld

def find_path(start_point, finish_point, world: KutuluWorld):
    choices = ((0,1), (1,0), (0,-1), (-1,0))
    g_dict = {start_point: 0}
    f_dict = {start_point: distance(start_point, finish_point)}
    common_candidates = [(f_dict[start_point], start_point)]
    close_set = set()
    pred_point = {}

    while len(common_candidates):
        point = heapq.heappop(common_candidates)[1]
        if point == finish_point:
            path = []
            while point != start_point:
                path.append(point)
                point = pred_point[point]
            return path

        close_set.add(point)
        for choise in choices:
            candidate = add(point, choise)
            if not world.is_empty(*candidate):
                continue
            g = g_dict[point] + 1
            h = distance(candidate, finish_point)
            f = g + h
            if candidate in close_set and g >= g_dict.get(candidate, 0):
                continue
            pred_point[candidate] = point
            if g < g_dict.get(candidate, 0):
                g_dict[candidate] = g
            if candidate in [x[1] for x in common_candidates]:
                continue
            assert candidate not in f_dict
            g_dict[candidate] = g
            f_dict[candidate] = f
            heapq.heappush(common_candidates, (f, candidate))
    assert False

def add(point1, point2):
    return (point1[0] + point2[0], point1[1] + point2[1])

def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

if __name__ == '__main__':
    world = KutuluWorld( 'map.txt' )
    points = [
        ((14,7), (10,11))
    ]
    for start, finish in points:
        for i,line in enumerate(world.map_grid):
            path = find_path(start, finish, world)
            line = ''.join(x if x != '.' else ' ' for x in list(line))
            for point in path:
                if i == point[1]:
                    line = list(line)
                    line[point[0]] = '.'
                    line = ''.join(line)
            if i == start[1]:
                line = list(line)
                line[start[0]] = 'S'
                line = ''.join(line)
            if i == finish[1]:
                line = list(line)
                line[finish[0]] = 'F'
                line = ''.join(line)
            print(line)
        print(path)
