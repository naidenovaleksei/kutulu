import random
from world.world import KutuluWorld


class BaseUnit():
    def __init__( self, unit_id, x, y, world: KutuluWorld ):
        self.x = x
        self.y = y
        self.id = unit_id
        self.world = world
        self.last_pos = None
        self.last_action = None
    
    def get_type(self):
        assert False
    
    def get_alive(self):
        return self.id is not None and self.world.is_empty(self.x, self.y)
    
    def get_action(self, entities):
        assert self.get_alive()
        return 'WAIT'

    def desc(self):
        assert False
    
    def finish(self):
        pass

    def update_state(self, units):
        pass

    # def make_action(self, entities):
    #     assert self.get_alive()
    #     action = self.get_action(entities)
    #     self._try_action(action)    
    
    def try_action(self, action: str):
        self.last_pos = (self.x, self.y)
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

    def _move(self, new_x, new_y):
        if not self.world.approve_move(self.x, self.y, new_x, new_y):
            raise Exception("bad new coords: %d %d" % (new_x, new_y))
        self.x, self.y = new_x, new_y


class UnitCollection():
    def __init__(self, unit_class):
        self.units = []
        self.unit_class = unit_class
        self.ids = 10
    
    def add_unit(self, *params):
        unit = self.unit_class(self.ids, *params)
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