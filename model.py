
from world.world import KutuluWorld
from world.world import SANITY_LOSS_LONELY, SANITY_LOSS_GROUP, WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME
from world.unit import BaseUnit, Explorer, Wanderer
from world.unit import SPAWNING, WANDERING
from players.player import PipePlayer

class KutuluModel:
    def __init__( self ):
        self.world = KutuluWorld( 'map.txt' )
        self.explorers = [ 
            Explorer(0, 6, 7, PipePlayer( 'submit.py' ), self.world),
            Explorer(1, 9, 7, PipePlayer( 'submit.py' ), self.world),
            Explorer(2, 6, 8, PipePlayer( 'submit.py' ), self.world)
         ]
        self.wanderers = []
    
    def make_turn( self ):
        live_explorers = [explorer for explorer in self.explorers if explorer.get_alive()]
        if len(live_explorers) == 0:
            return False
        for explorer in live_explorers:
            assert explorer.get_alive()
            explorer.make_action(live_explorers)

        for explorer in live_explorers:
            explorer.update_state(live_explorers)

        print([(explorer.id, explorer.sanity, explorer.last_action) for explorer in self.explorers])
        self.last_explorer = live_explorers[0]
        return True

    def finish(self):
        print("%d WIN!" % self.last_explorer.id)
        for explorer in self.explorers:
            explorer.finish()