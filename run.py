import time

from player import PipePlayer
from world import KutuluWorld
from model import KutuluModel
from view import View

player = PipePlayer( 'submit.py' )
world = KutuluWorld( 'map.txt' )
model = KutuluModel( world )
view = View( world, model )

player.init({
    'width': world.width(),
    'height': world.height(),
    'map_grid': world.map_grid,
    'const': world.get_consts()
})

# for i in range(3):
while (True):
    if not view.loop():
        break
    entities = [
        1,
        'EXPLORER 0 %d %d 250 2 3' % model.player_coords
    ]
    step = player.step({
        'entities': entities
    })
    print('STEP:', step, model.parse_step( step ))
    
    # --- Limit to 60 frames per second
    view.clock.tick(1)
    # time.sleep(5) 
else:
    print('finish')
    player.finish()
print('end')