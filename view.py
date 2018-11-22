# Import the pygame library and initialise the game engine
import pygame

from model import KutuluModel
from world import KutuluWorld, CELL_WALL, CELL_EMPTY, CELL_SPAWN
from car import BaseCell, MovingCell


# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

CELL_SIZE = 30

class View():
    def __init__(self, world: KutuluWorld, model: KutuluModel):
        pygame.init()

        # Open a new window
        width = world.width()
        height = world.height()
        self.size = (width * CELL_SIZE, height * CELL_SIZE)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("My First Game")
        
        # The clock will be used to control how fast the screen updates
        self.clock = pygame.time.Clock()

        self.cell_sprites_list = pygame.sprite.Group()
        for i in range(height):
            for j in range(width):
                color = {
                    CELL_WALL: BLACK,
                    CELL_EMPTY: GREEN,
                    CELL_SPAWN: BLUE
                }[ world.cell_type(j, i) ]
                cell = BaseCell(color, CELL_SIZE, CELL_SIZE)
                cell.rect.x = j * CELL_SIZE
                cell.rect.y = i * CELL_SIZE
                self.cell_sprites_list.add(cell)

        self.player_sprites_list = pygame.sprite.Group()
        self.player = BaseCell(RED, CELL_SIZE, CELL_SIZE)
        x,y = model.player_coords
        self.player.rect.x = x * CELL_SIZE
        self.player.rect.y = y * CELL_SIZE
        self.player_sprites_list.add( self.player )

        self.model = model
    
    def loop(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                print('QUIT')
                return False # Flag that we are done so we exit this loop
        screen = self.screen
        screen.fill(WHITE)
        player_cell = self.player
        player_coords = self.model.player_coords
        player_cell.rect.x = player_coords[0] * CELL_SIZE
        player_cell.rect.y = player_coords[1] * CELL_SIZE
        print(self.player.rect.x, self.player.rect.y)
        # self.player_sprites_list = pygame.sprite.Group()
        # self.player_sprites_list.add( self.player )

        self.cell_sprites_list.draw(screen)
        self.player_sprites_list.update()
        self.player_sprites_list.draw(screen)


        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # pygame.time.delay( 1000 )

        return True
    
