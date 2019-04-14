
# ALLOWED_COMMANDS = [
#     'WAIT',
#     'MOVE %d %d'
# ]
from world.world import KutuluWorld
from world.world import SANITY_LOSS_LONELY, SANITY_LOSS_GROUP, WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME
from world.unit import BaseUnit, Explorer, Wanderer
from world.unit import SPAWNING, WANDERING
from players.player import PipePlayer

class KutuluModel:
    def __init__( self ):
        self.world = KutuluWorld( 'map.txt' )
        self.explorers = [ 
            Explorer(0, 6, 7, PipePlayer( 'submit.py' ), self.world)
         ]
        self.wanderers = []
    
    def make_turn( self ):
        entities = [ explorer.desc() for explorer in self.explorers ]
        print(entities)
        for explorer in self.explorers:
            explorer.make_action(entities)

        entities = [ explorer.desc() for explorer in self.explorers ]
        for explorer in self.explorers:
            explorer.update_state()

    def finish(self):
        for explorer in self.explorers:
            explorer.finish()