map_grid = []
with open('map.txt', 'r') as f:
    map_grid = [x.strip() for x in f.readlines()]

# print(map_grid)

class MapGrid():
    def __init__(self, map_grid):
        self.map_grid = map_grid
    
    def cell(self, x, y):
        return self.map_grid[y][x]
    
    def width(self):
        return len(self.map_grid[0])
    
    def height(self):
        return len(self.map_grid)

map_grid = MapGrid(map_grid)