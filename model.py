
# ALLOWED_COMMANDS = [
#     'WAIT',
#     'MOVE %d %d'
# ]
from world import KutuluWorld

class KutuluModel:
    def __init__( self, world:KutuluWorld ):
        self.world = world
        self.player_coords = (6,7)

    def parse_step( self, step: str ):
        ops = step.split()
        if ops[0] == 'WAIT':
            return self.do_step('WAIT')
        elif ops[0] == 'MOVE':
            x = int(ops[1])
            y = int(ops[2])
            return self.do_step('MOVE', x, y)
        else:
            assert False
    
    def do_step( self, action, *ops):
        if action == 'WAIT':
            return True
        elif action == 'MOVE':
            x, y = ops
            return self._move_player(x, y)

    def distance( self, x1, y1, x2, y2 ):
        return abs(x1 - x2) + abs(y1 - y2)

    def _check_move( self, x, y ):
        x_old, y_old = self.player_coords
        if self.distance(x, y, x_old, y_old) != 1:
            return False
        return self.world.is_empty(x, y)
    
    def _move_player( self, x, y ):
        if not self._check_move(x, y):
            return False
        self.player_coords = (x, y)
        return True