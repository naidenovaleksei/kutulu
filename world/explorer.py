import random

from world.unit import BaseUnit
from world.world import KutuluWorld
from world.world import SANITY_LOSS_LONELY, SANITY_LOSS_GROUP, SANITY_LOSS_SPOOKED
from world.world import WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME, WANDERING


class Explorer( BaseUnit ):
    def __init__( self, unit_id, x, y, player, world: KutuluWorld ):
        super(Explorer, self).__init__(unit_id, x, y, world)
        self.sanity = 250
        self.player = player
        self.init_player(world)
    
    def get_type(self):
        return "EXPLORER"
    
    def get_alive(self):
        if not super(Explorer, self).get_alive():
            return False
        return self.sanity > 0
    
    def get_action(self, entities):
        assert self.get_alive()
        if self.player is None:
            return 'WAIT'
        world_data = self._get_world_data(entities)
        action = self.player.step(world_data)
        return action

    def desc(self):
        desc = f'{self.get_type()} {self.id} {self.x} {self.y} {self.sanity} 0 0'
        return desc

    def finish(self):
        super(Explorer, self).finish()
        if self.player is not None:
            self.player.finish()

    def update_state(self, units):
        super(Explorer, self).update_state(units)
        no_neighbours = True
        explorers = [unit for unit in units if unit.get_type() == 'EXPLORER']
        wanderers = [unit for unit in units if unit.get_type() == 'WANDERER']

        for wanderer in wanderers:
            if wanderer.state != WANDERING:
                continue
            if self._get_catched(wanderer):
                self.sanity = max(self.sanity - SANITY_LOSS_SPOOKED, 0)
                print('wanderer %d spooked' % wanderer.id)
                wanderer.spooked = True

        for explorer in explorers:
            if explorer.id != self.id and \
                self.world.distance(self.x, self.y, explorer.x, explorer.y) <= 2:
                no_neighbours = False
                break
        sanity_loss = SANITY_LOSS_LONELY if no_neighbours else SANITY_LOSS_GROUP
        self.sanity = max(self.sanity - sanity_loss, 0)
        if not self.get_alive():
            self.finish()
        return

    def init_player(self, world: KutuluWorld):   
        if self.player is None:
            return
        self.player.init({
            'width': world.width(),
            'height': world.height(),
            'map_grid': world.map_grid,
            'const': (SANITY_LOSS_LONELY, SANITY_LOSS_GROUP, WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME)
        })
    
    def _get_catched(self, wanderer):
        if wanderer.x == self.x and wanderer.y == self.y:
            return True
        if self.last_pos == (wanderer.x, wanderer.y) and \
            wanderer.last_pos == (self.x, self.y):
            return True
        return False

    def _get_world_data(self, explorers):
        entity_count = len(explorers)
        explorers = [explorer for explorer in explorers if explorer.id != self.id]
        assert len(explorers) == entity_count - 1
        entities = [explorer.desc() for explorer in explorers]
        entities = [entity_count, self.desc()] + entities
        world_data = {'entities': entities}
        return world_data