
# ALLOWED_COMMANDS = [
#     'WAIT',
#     'MOVE %d %d'
# ]
from world import KutuluWorld
from world import SANITY_LOSS_LONELY, SANITY_LOSS_GROUP, WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME
from unit import BaseUnit, Explorer, Wanderer
from unit import SPAWNING, WANDERING

class KutuluModel:
    def __init__( self, world:KutuluWorld ):
        self.world = world
        self.player_coords = (6,7)
        self.counter = 0
        self.explorers = []
        self.wanderers = []

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
    
    def make_turn( self ):
        for i, explorer in enumerate( self.explorers ):
            have_neighbours = False
            for j, explorer2 in enumerate( self.explorers ):
                x1, y1 = explorer.coords
                x2, y2 = explorer2.coords
                if i != j and self.distance( x1, y1, x2, y2 ) <= 2:
                    have_neighbours = True
                    break
            if have_neighbours:
                explorer.sanity -= 1
            else:
                explorer.sanity -= 3
                
        for wanderer in self.wanderers:
            if wanderer.state == SPAWNING:
                wanderer.spawn_time -= 1
                if wanderer.spawn_time == 0:
                    wanderer.spawn_time = None
                    wanderer.state = WANDERING
                    wanderer.life_time = WANDERER_LIFE_TIME
            elif wanderer.state == WANDERING:
                wanderer.life_time -= 1
                if wanderer.life_time == 0:
                    wanderer.life_time = None
                    wanderer.state = SPAWNING
                    wanderer.spawn_time = WANDERER_SPAWN_TIME

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