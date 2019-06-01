import random
from world.world import KutuluWorld
from world.world import SANITY_LOSS_LONELY, SANITY_LOSS_GROUP, SANITY_LOSS_SPOOKED, WANDERER_SPAWN_TIME, WANDERER_LIFE_TIME

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
        self.last_action = action
        try:
            ops = action.split()
            if ops[0] == 'WAIT':
                pass
            elif ops[0] == 'MOVE':
                x, y = [int(x) for x in ops[1:]]
                self._move(x, y)
            else:
                raise Exception("%d bad action: %s" % (self.id, action))
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
        assert self.get_alive()
        action = self.get_action(entities)
        self._try_action(action)

    def update_state(self, units):
        no_neighbours = True
        explorers = [unit for unit in units if unit.get_type() == 'EXPLORER']
        wanderers = [unit for unit in units if unit.get_type() == 'WANDERER']

        for wanderer in wanderers:
            if wanderer.state != WANDERING:
                continue
            if wanderer.x == self.x and wanderer.y == self.y:
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

    def get_world_data(self, explorers):
        entity_count = len(explorers)
        explorers = [explorer for explorer in explorers if explorer.id != self.id]
        assert len(explorers) == entity_count - 1
        entities = [explorer.desc() for explorer in explorers]
        entities = [entity_count, self.desc()] + entities
        world_data = {'entities': entities}
        return world_data

    def desc(self):
        desc = f'{self.get_type()} {self.id} {self.x} {self.y} {self.sanity} 0 0'
        return desc
    
    def get_alive(self):
        return self.sanity > 0

    def finish(self):  
        if self.player is not None:
            self.player.finish()
    
    def get_type(self):
        return "EXPLORER"


class Wanderer( BaseUnit ):
    def __init__( self, x, y, world: KutuluWorld ):
        super(Wanderer, self).__init__(x, y)
        self.spawn_time = WANDERER_SPAWN_TIME
        self.life_time = None
        self.state = SPAWNING
        self.id = -1
        self.spooked = False
        self.world = world

    def _move(self, new_x, new_y):
        if not self.world.approve_move(self.x, self.y, new_x, new_y):
            raise Exception("bad new coords: %d %d" % (new_x, new_y))
        self.x, self.y = new_x, new_y
    
    def _try_action(self, action: str):
        self.last_action = action
        try:
            ops = action.split()
            if ops[0] == 'WAIT':
                pass
            elif ops[0] == 'MOVE':
                x, y = [int(x) for x in ops[1:]]
                self._move(x, y)
            else:
                raise Exception("%d bad action: %s" % (self.id, action))
        except Exception as e:
            print(e)

    def make_action(self, entities):
        assert self.get_alive()
        # action = random.choice([
        #     "MOVE %d %d" % (self.x + 1, self.y),
        #     "MOVE %d %d" % (self.x - 1, self.y),
        #     "MOVE %d %d" % (self.x, self.y + 1),
        #     "MOVE %d %d" % (self.x, self.y - 1)
        # ])
        x,y = self.x,self.y
        cases = []
        for _x,_y in [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]:
            if self.world.is_empty(_x, _y):
                cases.append('MOVE %d %d' % (_x, _y))
        action = random.choice(cases)
        self._try_action(action)

    def update_state(self, explorers):
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
    
    def get_type(self):
        return "WANDERER"
    
    def get_alive(self):
        if self.state == WANDERING:
            return self.life_time > 0 and not self.spooked
        elif self.state == SPAWNING:
            return True
        assert False

    def desc(self):
        ltime = self.spawn_time if self.state == SPAWNING else self.life_time
        desc = f'{self.get_type()} {self.id} {self.x} {self.y} {ltime} {self.state} 0'
        return desc
    
    def finish(self):
        pass


class UnitCollection():
    def __init__(self, unit_class):
        self.units = []
        self.unit_class = unit_class
        self.ids = 10
    
    def add_unit(self, *params):
        unit = self.unit_class(*params)
        unit.id = self.ids
        self.ids += 1
        self.units.append(unit)
    
    def __iter__(self):
        return iter(self.units)
    
    def update_state(self):
        for unit in self.units:
            if not unit.get_alive():
                print('wanderer %d finish' % unit.id)
                unit.finish()
        self.units = [unit for unit in self.units if unit.get_alive()]

    # def start_spawn_wanderer(self, explorers, first_time=True):
    #     if first_time:
    #         spawnpoints = self.world.get_all_spawnpoints()
    #     else:
    #         explorers_coords = [(e.x, e.y) for e in explorers]
    #         spawnpoints = self.world.get_furthest_spawnpoints(explorers_coords)
    #     for spawnpoint in spawnpoints:
    #         wanderer = Wanderer(*spawnpoint)
    #         self.wanderers.append(wanderer)