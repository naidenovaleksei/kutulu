import sys
import math
import numpy as np

print('hola!', file=sys.stderr)
width = int(input())
height = int(input())
lines = []
for i in range(height):
    line = input()
    lines.append( line )
    print(line, file=sys.stderr)

# sanity_loss_lonely: how much sanity you lose every turn when alone, always 3 until wood 1
# sanity_loss_group: how much sanity you lose every turn when near another player, always 1 until wood 1
# wanderer_spawn_time: how many turns the wanderer take to spawn, always 3 until wood 1
# wanderer_life_time: how many turns the wanderer is on map after spawning, always 40 until wood 1
sanity_loss_lonely, sanity_loss_group, wanderer_spawn_time, wanderer_life_time = [int(i) for i in input().split()]

# game loop
while True:
    entity_count = int(input())  # the first given entity corresponds to your explorer
    cases = ['WAIT']
    for i in range(entity_count):
        entity_type, id, x, y, param_0, param_1, param_2 = input().split()
        # print((entity_type, id, x, y, param_0, param_1, param_2), file=sys.stderr)
        id = int(id)
        x = int(x)
        y = int(y)
        param_0 = int(param_0)
        param_1 = int(param_1)
        param_2 = int(param_2)
        if i == 0:
            for _x,_y in [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]:
                if lines[_y][_x] == '.':
                    cases.append('MOVE %d %d' % (_x, _y))
    
    print(np.random.choice(cases))