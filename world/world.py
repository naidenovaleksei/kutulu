CELL_EMPTY = '.'
CELL_WALL = '#'
CELL_SPAWN = 'w'

SANITY_LOSS_LONELY = 3
SANITY_LOSS_GROUP = 1
WANDERER_SPAWN_TIME = 3
WANDERER_LIFE_TIME = 40

class KutuluWorld():
    def __init__(self, fname='map.txt'):
        with open(fname, 'r') as f:
            self.map_grid = [ x.strip() for x in f.readlines() ]
    
    def cell(self, x, y):
        return self.map_grid[y][x]
    
    def is_empty(self, x, y):
        return self.cell(x,y) in (CELL_EMPTY, CELL_SPAWN)

    def cell_type(self, x, y):
        return self.cell(x,y)
    
    def width(self):
        return len(self.map_grid[0])
    
    def height(self):
        return len(self.map_grid)

    def distance( self, x1, y1, x2, y2 ):
        return abs(x1 - x2) + abs(y1 - y2)
    
    def approve_move(self, old_x, old_y, new_x, new_y):
        if self.distance(old_x, old_y, new_x, new_y) != 1:
            return False
        return self.is_empty(new_x, new_y)
