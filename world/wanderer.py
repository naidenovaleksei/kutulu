import random

from world.unit import BaseUnit
from world.world import KutuluWorld
from world.world import WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME, SPAWNING, WANDERING


class Wanderer( BaseUnit ):
    def __init__( self, unit_id, x, y, world: KutuluWorld ):
        super(Wanderer, self).__init__(unit_id, x, y, world)
        self.spawn_time = WANDERER_SPAWN_TIME
        self.life_time = None
        self.state = SPAWNING
        self.id = -1
        self.spooked = False
        self.world = world
    
    def get_type(self):
        return "WANDERER"
    
    def get_alive(self):
        if not super(Wanderer, self).get_alive():
            return False
        if self.state == WANDERING:
            return self.life_time > 0 and not self.spooked
        elif self.state == SPAWNING:
            return True
        assert False

    def get_action(self, entities):
        x,y = self.x,self.y
        cases = []
        for _x,_y in [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]:
            if self.world.is_empty(_x, _y):
                cases.append('MOVE %d %d' % (_x, _y))
        action = random.choice(cases)
        return action

    def desc(self):
        ltime = self.spawn_time if self.state == SPAWNING else self.life_time
        desc = f'{self.get_type()} {self.id} {self.x} {self.y} {ltime} {self.state} 0'
        return desc

    def update_state(self, units):
        super(Wanderer, self).update_state(units)
        if self.state == SPAWNING:
            self.spawn_time -= 1
        elif self.state == WANDERING and self.life_time > 0:
            self.life_time -= 1
        else:
            assert False
        if (self.spawn_time == 0) and (self.state == SPAWNING):
            print('wanderer %d spawned and wandering' % self.id)
            self.state = WANDERING
            self.life_time = WANDERER_LIFE_TIME