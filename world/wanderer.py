import random

from world.unit import BaseUnit
from world.world import KutuluWorld
from world.world import WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME, SPAWNING, WANDERING
from world.path import find_path


class Wanderer( BaseUnit ):
    def __init__( self, unit_id, x, y, world: KutuluWorld ):
        super(Wanderer, self).__init__(unit_id, x, y, world)
        self.spawn_time = WANDERER_SPAWN_TIME
        self.life_time = None
        self.state = SPAWNING
        self.spooked = False
        self.world = world
        self.target = -1
    
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
        assert self.get_alive()
        x,y = self.x, self.y
        if self.state == SPAWNING:
            return 'WAIT'
        try:
            target = [unit for unit in entities if unit.id == self.target][0]
            path = find_path((x, y), (target.x, target.y), self.world)
            action = 'MOVE %d %d' % (path[-1])
        except IndexError:
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
            if self.target < 0:
                self.choose_target(units)
            self.life_time -= 1
        else:
            assert False
        if (self.spawn_time == 0) and (self.state == SPAWNING):
            print('wanderer %d spawned and wandering' % self.id)
            self.state = WANDERING
            self.life_time = WANDERER_LIFE_TIME
    
    def get_distance(self, unit):
        return self.world.distance(self.x, self.y, unit.x, unit.y)

    
    def choose_target(self, units):
        explorers = [unit for unit in units if unit.get_type() == 'EXPLORER']
        # TODO: min path is needed
        target_unit = min(explorers, key=self.get_distance)
        self.target = target_unit.id

