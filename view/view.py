# Import the pygame library and initialise the game engine
import pygame

from model import KutuluModel
from world.world import KutuluWorld, CELL_WALL, CELL_EMPTY, CELL_SPAWN
from view.cells import BaseCell


# Define some colors
EMPTY_COLOR = ( 255, 255, 255)
WALL_COLOR = ( 127, 127, 127)
SPAWN_COLOR = ( 0, 0, 255)
WANDERER_COLOR = (0, 255, 0)
EXPLORER_COLORS = [
    ( 200, 100, 0),
    ( 100, 0, 200),
    ( 100, 200, 200),
    ( 100, 200, 0)
]
WHITE = ( 255, 255, 255)
BLACK = (0, 0, 0)

CELL_SIZE = 30

class View():
    def __init__(self, model: KutuluModel):
        pygame.init()

        world = model.world
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
                    CELL_WALL: WALL_COLOR,
                    CELL_EMPTY: EMPTY_COLOR,
                    CELL_SPAWN: SPAWN_COLOR
                }[ world.cell_type(j, i) ]
                cell = BaseCell(color, CELL_SIZE, CELL_SIZE)
                cell.rect.x = j * CELL_SIZE
                cell.rect.y = i * CELL_SIZE
                self.cell_sprites_list.add(cell)

        self.player_sprites_list = pygame.sprite.Group()
        # self.player_list = []
        for unit in model.explorers:
            # unit_color = WHITE if unit.get_type() == "EXPLORER" else RED
            unit_color = EXPLORER_COLORS[unit.id % 4]
            unit_cell = BaseCell(unit_color, CELL_SIZE, CELL_SIZE)
            unit_cell.rect.x = unit.x * CELL_SIZE
            unit_cell.rect.y = unit.y * CELL_SIZE
            self.player_sprites_list.add( unit_cell )
            # self.player_list.append( unit_cell )

        self.model = model
    
    def loop(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                print('QUIT')
                return False # Flag that we are done so we exit this loop
        screen = self.screen
        screen.fill(WHITE)
        self.cell_sprites_list.draw(screen)

        font = pygame.font.SysFont('Comic Sans MS', 10)
        text_color = BLACK
        for i in range(self.model.world.height()):
            text = font.render(f"{i}", True, text_color)
            screen.blit(text, (0, i * CELL_SIZE))
        for i in range(self.model.world.width()):
            text = font.render(f"{i}", True, text_color)
            screen.blit(text, (i * CELL_SIZE, 0))

        for unit, unit_cell in zip(self.model.explorers, self.player_sprites_list):
            if unit.get_alive():
                unit_cell.rect.x = unit.x * CELL_SIZE
                unit_cell.rect.y = unit.y * CELL_SIZE
                # print(unit_cell.rect.x, unit_cell.rect.y)
            else:
                unit_cell.rect.x =  self.model.world.width() * CELL_SIZE
                unit_cell.rect.y = self.model.world.height() * CELL_SIZE
            text = f"{unit.id}: {unit.sanity}"
            font = pygame.font.SysFont('Comic Sans MS', 10)
            text_color = EXPLORER_COLORS[unit.id % 4]
            text = font.render(text, True, text_color)
            screen.blit(text, (self.size[0] - 100, 100 + 10 * unit.id))

        self.player_sprites_list.update()
        self.player_sprites_list.draw(screen)

        self.wanderers_sprites_list = pygame.sprite.Group()
        for unit in self.model.wanderers:
            unit_color = WANDERER_COLOR
            unit_cell = BaseCell(unit_color, CELL_SIZE, CELL_SIZE)
            unit_cell.rect.x = unit.x * CELL_SIZE
            unit_cell.rect.y = unit.y * CELL_SIZE
            self.wanderers_sprites_list.add( unit_cell )

        self.wanderers_sprites_list.update()
        self.wanderers_sprites_list.draw(screen)


        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # pygame.time.delay( 1000 )

        return True
    
