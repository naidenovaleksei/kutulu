
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
            Explorer(2, 6, 8, PipePlayer( 'submit.py' ), self.world)
         ]
        self.wanderers = UnitCollection(Wanderer)
        self.turn_count = 0
    
    def make_turn( self ):
        if not self.get_continue():
            return False

        entities = self.get_alive_explorers() + self.wanderers.units
        for explorer in entities:
            assert explorer.get_alive()
            explorer.make_action(entities)

        # if self.turn_count % 5 == 0
        if self.turn_count == 0:
            self.start_spawn_wanderer()

        # live_wanderers = [wanderer for wanderer in self.wanderers if wanderer.get_alive()]
        for unit in entities:
            unit.update_state(entities)
        
        self.wanderers.update_state()

        # print([(explorer.id, explorer.sanity, explorer.last_action) for explorer in self.explorers])
        self.last_explorer = self.get_alive_explorers()[0]
        self.turn_count += 1
        return True
    
    def get_alive_explorers(self):
        res = [explorer for explorer in self.explorers if explorer.get_alive()]
        return res
    
    def get_continue(self):
        res = next((True for wanderer in self.get_alive_explorers()), False)
        return res

    def finish(self):
        print("%d WIN!" % self.last_explorer.id)
        for explorer in self.explorers:
            explorer.finish()

    def start_spawn_wanderer(self):
        spawnpoints = self.world.get_all_spawnpoints()
        for x,y in spawnpoints:
            self.wanderers.add_unit(x, y, self.world)