
from world.world import KutuluWorld
from world.world import SANITY_LOSS_LONELY, SANITY_LOSS_GROUP, WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME
from world.explorer import Explorer
from world.wanderer import Wanderer
from world.unit import UnitCollection
from world.world import SPAWNING, WANDERING
from players.player import PipePlayer

class KutuluModel:
    def __init__( self ):
        self.world = KutuluWorld( 'map.txt' )
        self.explorers = [ 
            Explorer(0, 6, 7, PipePlayer( 'submit.py' ), self.world),
            Explorer(1, 5, 3, PipePlayer( 'submit.py' ), self.world),
            Explorer(2, 6, 9, PipePlayer( 'submit.py' ), self.world)
         ]
        self.wanderers = UnitCollection(Wanderer)
        self.turn_count = 0
        self.last_explorer = None
    
    def make_turn( self ):
        entities = self.get_alive_explorers() + self.wanderers.units
        actions = []
        # сначала собираем все действия
        for explorer in entities:
            assert explorer.get_alive()
            actions.append(explorer.get_action(entities))

        # потом выполняем все действия
        for unit,action in zip(entities, actions):
            unit.try_action(action)

        if self.turn_count % 5 == 0:
            first_time = self.turn_count == 0
            self.start_spawn_wanderer(first_time)

        live_wanderers = [wanderer for wanderer in self.wanderers if wanderer.get_alive()]
        entities = self.get_alive_explorers() + live_wanderers
        for unit in entities:
            unit.update_state(entities)
        
        self.wanderers.update_state()

        if not self.get_continue():
            self.last_explorer = self.get_alive_explorers()[0]
            return False
        
        self.turn_count += 1
        return True
    
    def get_alive_explorers(self):
        res = [explorer for explorer in self.explorers if explorer.get_alive()]
        return res
    
    def get_continue(self):
        explorers = self.get_alive_explorers()
        return len(explorers) > 1

    def finish(self):
        print("%d WIN!" % self.last_explorer.id)
        for explorer in self.explorers:
            explorer.finish()

    def start_spawn_wanderer(self, first_time=True):
        if first_time:
            spawnpoints = self.world.get_all_spawnpoints()
        else:
            explorers_coords = [(e.x, e.y) for e in self.get_alive_explorers()]
            spawnpoints = self.world.get_furthest_spawnpoints(explorers_coords)
        for x,y in spawnpoints:
            self.wanderers.add_unit(x, y, self.world)