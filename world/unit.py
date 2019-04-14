from world.world import KutuluWorld
from world.world import SANITY_LOSS_LONELY, SANITY_LOSS_GROUP, WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME

SPAWNING = 0
WANDERING = 1

class BaseUnit():
    def __init__( self, x, y ):
        self.x = x
        self.y = y

class Explorer( BaseUnit ):
    def __init__( self, unit_id, x, y, player, world: KutuluWorld ):
        super(Explorer, self).__init__(x, y)
        self.sanity = 250
        self.player = player
        self.x = x
        self.y = y
        self.id = unit_id
        self.world = world
        self.init_player(world)

    def _move(self, new_x, new_y):
        if not self.world.approve_move(self.x, self.y, new_x, new_y):
            raise Exception("bad new coords: %d %d" % (new_x, new_y))
        self.x, self.y = new_x, new_y
    
    def _try_action(self, action: str):
        try:
            ops = action.split()
            if ops[0] == 'WAIT':
                print('WAIT')
            elif ops[0] == 'MOVE':
                x, y = [int(x) for x in ops[1:]]
                self._move(x, y)
                print('MOVE', x, y)
            else:
                raise Exception("bad action: %s" % action)
        except Exception as e:
            print(e)

    def init_player(self, world: KutuluWorld):   
        if self.player is None:
            return
        self.player.init({
            'width': world.width(),
            'height': world.height(),
            'map_grid': world.map_grid,
            'const': (SANITY_LOSS_LONELY, SANITY_LOSS_GROUP, WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME)
        })
    
    def get_action(self, entities):  
        if self.player is None:
            return 'WAIT'
        world_data = self.get_world_data(entities)
        action = self.player.step(world_data)
        return action
    
    def make_action(self, entities):
        action = self.get_action(entities)
        self._try_action(action)

    def update_state(self):
        return

    def get_world_data(self, entities):
        entity_count = len(entities)
        entities = [entity for i,entity in enumerate(entities) if i != self.id]
        entities = [entity_count, self.desc()] + entities
        world_data = {'entities': entities}
        return world_data

    def desc(self):
        desc = f'{self.get_type()} {self.id} {self.x} {self.y} {self.sanity} 0 0'
        return desc

    def finish(self):  
        if self.player is not None:
            self.player.finish()
    
    def get_type(self):
        return "EXPLORER"


class Wanderer( BaseUnit ):
    def __init__( self, x, y ):
        super(Wanderer, self).__init__(x, y)
        self.spawn_time = None
        self.life_time = None
        self.state = SPAWNING
