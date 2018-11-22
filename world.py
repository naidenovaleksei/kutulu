CELL_EMPTY = '.'
CELL_WALL = '#'
CELL_SPAWN = 'w'


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
    
    def get_consts(self):
        sanity_loss_lonely = 3
        sanity_loss_group = 1
        wanderer_spawn_time = 3
        wanderer_life_time = 40
        return (sanity_loss_lonely, sanity_loss_group, wanderer_spawn_time, wanderer_life_time)

