"""
This module contains the different classes
which manage the game itself.
"""

import collections
import sys
import pygame
from constants import (BACKGROUND_TEXTURES_PATH, CHARACTER,
                       CHARACTER_DIRECTIONS, CHARACTERS_INFO, CRATE,
                       GAME_BUTTONS_HEIGHT, GAME_BUTTONS_WIDTH,
                       GAME_BUTTONS_Y_MARGIN, RED_CRATE, TILE_SIZE, TROPHY,
                       WINDOW_SIZE, WINDOW_TILE_SIZE, CHARACTER_DIRECTIONS_OPPOSITE)
from user_interface import Button


def load_background_texture(tile_code):
    """Utility function loading the texture of
    a certin tile in the background textures"""

    # Textures of the background
    background_textures = pygame.image.load(BACKGROUND_TEXTURES_PATH).convert_alpha()

    # We intialize the resulting texture
    result = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    # We extract the portion we want
    result.blit(
        background_textures,
        (0, 0),
        pygame.Rect(tile_code * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
    )

    return result

class BackgroundManager(pygame.sprite.Sprite):
    """Class managing the background of the game."""
    def __init__(self):
        """Constructor method. It initializes the different attributes of the background."""

        # We first call the parent constructor
        pygame.sprite.Sprite.__init__(self)

        # Initial coordinates of the character
        self.initial_character_coords = ()

        # Initial coordinates of the crates and trophies on the map
        self.initial_crates, self.initial_trophies = [], []

        # Codes of the tiles of the background map
        self.background_map = []

        # Image of the background
        self.image = pygame.Surface(WINDOW_SIZE)
        self.rect = pygame.Rect((0, 0), WINDOW_SIZE)

    def parse(self, filename):
        """Method parsing the background image from a level file."""

        # We reset the different attributes, so that the user can call this method multiple times
        self.initial_crates, self.initial_trophies, self.background_map = [], [], []

        # Variable containing the textures used for the background image
        background_textures = pygame.image.load(BACKGROUND_TEXTURES_PATH).convert()

        # Variable used to report an error
        error = False

        # We open the level file to extract its data
        with open('levels/{}'.format(filename), 'r') as level_file:
            for line in level_file:
                # We first extract the codes of this line as a list of string objects
                # The codes of the tiles are separated with comas
                tile_codes = line.split(',')

                # We check if the line contains the required number of tiles
                if len(tile_codes) != WINDOW_TILE_SIZE:
                    error = True
                    break

                # We convert the string values into integers
                try:
                    for index, value in enumerate(tile_codes):
                        tile_codes[index] = int(value)

                        # If the integer is not between 0 and 5, we raise a value error
                        if not 0 <= tile_codes[index] <= CHARACTER:
                            raise ValueError

                except ValueError:
                    error = True
                    break

                self.background_map.append(tile_codes)

        # If an error occured, or if the number of lines is not valid, we return False
        if error or len(self.background_map) != WINDOW_TILE_SIZE:
            return False

        # Now we create the background image from the <background_map> variable
        for row in range(WINDOW_TILE_SIZE):
            for column in range(WINDOW_TILE_SIZE):
                # Variable containing the code of the tile we will finally display
                displayed_tile = 0

                # If the tile code corresponds to a crate or a trophy,
                # we do not want to add it to the background.
                # Instead, we store its coordinates for later use
                if self.background_map[row][column] == CRATE:
                    self.initial_crates.append((column, row))

                elif self.background_map[row][column] == TROPHY:
                    self.initial_trophies.append((column, row))

                elif self.background_map[row][column] == CHARACTER:
                    self.initial_character_coords = (column, row)

                else:
                    displayed_tile = self.background_map[row][column]

                # We erase the crates, trophies, and character from the <background_map> variable
                # (we have already stored their coordinates in other variables)
                self.background_map[row][column] = displayed_tile

                # Coordinates of the tile in the background
                dest_coord = (column * TILE_SIZE, row * TILE_SIZE)

                # Rectangle defining the portion of the
                # background textures taken by the tile we want
                source_rect = pygame.Rect(TILE_SIZE * displayed_tile, 0, TILE_SIZE, TILE_SIZE)

                # Finally, we copy this portion of the textures in
                # the background image, at the computed coordinates
                self.image.blit(background_textures, dest_coord, source_rect)

        return True

class Character(pygame.sprite.Sprite):
    """Class managing the character in the game"""
    def __init__(self, column, row, character_id):
        """Constructor mathod. It initializes the character depending on the given <character_id>"""

        # We first call the parent constructor
        pygame.sprite.Sprite.__init__(self)

        # Coordinates of the character (on the map, not on the screen)
        self.column, self.row = column, row

        # Rect (coordinates and dimensions) of the character
        self.rect = pygame.Rect(
            self.column * TILE_SIZE + (TILE_SIZE - CHARACTERS_INFO[character_id]['width']) // 2,
            self.row * TILE_SIZE  + (TILE_SIZE - CHARACTERS_INFO[character_id]['height']) // 2,
            CHARACTERS_INFO[character_id]['width'],
            CHARACTERS_INFO[character_id]['height']
        )

        # Initial direction of the character
        self.direction = pygame.K_DOWN

        # Textures of the character
        self.textures = pygame.image.load(CHARACTERS_INFO[character_id]['textures_path'])
        self.textures.convert_alpha()

        # Rectangle defining the portion of the textures that we will display
        source_rect = pygame.Rect(
            self.rect.width * CHARACTER_DIRECTIONS[self.direction]['texture_pos'], 0,
            self.rect.width, self.rect.height
        )

        # Rendered image of the character
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.blit(self.textures, (0, 0), source_rect)

    def change_coords(self, next_column, next_row):
        """Method changing the coordinates of the character."""
        self.column, self.row = next_column, next_row

        # We update the coordinates of the character
        self.rect.x = self.column * TILE_SIZE + (TILE_SIZE - self.rect.width) // 2
        self.rect.y = self.row * TILE_SIZE  + (TILE_SIZE - self.rect.height) // 2

        # Rectangle defining the portion of the textures that we will display
        source_rect = pygame.Rect(
            self.rect.width * CHARACTER_DIRECTIONS[self.direction]['texture_pos'], 0,
            self.rect.width, self.rect.height
        )

        # Finally, we update the displayed image of the character
        self.image.fill(pygame.Color(0, 0, 0, 0))
        self.image.blit(self.textures, (0, 0), source_rect)

    def update(
            self,
            direction,
            level_tile_map,
            crates, trophies,
            move_queue,
            reverse=False,
            with_crate=False
        ):
        """Method moving the character with the given <direction> parameter.
        It also requires the <level_tile_map>, <crates> and <trophies>
        parameters, for collisions. The <move_queue> parameter is usefull
        for storing the moves of the character. The <reversed> and <with_crate>
        parameters are used when the move is backward."""

        # First, we set up the new direction
        self.direction = direction

        # Then we compute the next coordinates, taking in account the <reverse> parameter
        direction_coeff = -1 if reverse else 1

        next_column = self.column + direction_coeff * CHARACTER_DIRECTIONS[self.direction]['dx']
        next_row = self.row + direction_coeff * CHARACTER_DIRECTIONS[self.direction]['dy']

        # Variable which saves if the collisions with the crates are not problematic
        collision_ok, crate_collision = True, False

        if reverse:
            if with_crate:
                # We have to move the crate that was previously moved
                # These are the coordinates of the character if the move was forward
                column_forward = self.column + CHARACTER_DIRECTIONS[self.direction]['dx']
                row_forward = self.row + CHARACTER_DIRECTIONS[self.direction]['dy']

                for crate in crates:
                    if crate.column == column_forward and crate.row == row_forward:
                        crate.update(
                            CHARACTER_DIRECTIONS_OPPOSITE[direction],
                            level_tile_map,
                            crates,
                            trophies
                        )

        else:
            # We check for the collision with any crate
            for crate in crates:
                if crate.column == next_column and crate.row == next_row:
                    collision_ok = crate.update(direction, level_tile_map, crates, trophies)
                    crate_collision = True

        # We check if the next tile is an empty one
        if not level_tile_map[next_row][next_column] and collision_ok:
            # We change the coordinates of the character
            self.change_coords(next_column, next_row)

            if not reverse:
                # We store the move in the queue
                move_queue.append((self.direction, crate_collision))

class Crate(pygame.sprite.Sprite):
    """Class managing a crate in the game."""

    @staticmethod
    def load_textures():
        """Static method loading the textures of the crates (regular and red)"""
        Crate.regular_crate_texture = load_background_texture(CRATE)
        Crate.red_crate_texture = load_background_texture(RED_CRATE)

    def __init__(self, column, row):
        """Constructor method. It initializes the coordinates of the crate."""

        # We first call the parent constructor
        pygame.sprite.Sprite.__init__(self)

        # Coordinates of the crate (in the map, not on the screen)
        self.column, self.row = column, row

        # Rect (coordinates and dimensions) of the crate
        self.rect = pygame.Rect(
            self.column * TILE_SIZE,
            self.row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        # Displayed image of the crate
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.blit(Crate.regular_crate_texture, (0, 0))
    
    def change_coords(self, next_column, next_row, trophies):
        """Method changing the coordinates of the crate."""

        # We edit the map coordinates of the crate
        self.column, self.row = next_column, next_row

        # Then, we edit the real coordinates of the crate
        self.rect.x = self.column * TILE_SIZE
        self.rect.y = self.row * TILE_SIZE

        # If the crate is on a trophy, then it becomes red
        if (self.column, self.row) in trophies:
            self.image.blit(Crate.red_crate_texture, (0, 0))

        else:
            self.image.blit(Crate.regular_crate_texture, (0, 0))

    def update(self, direction, level_tile_map, crates, trophies):
        """Method moving the crate with the given <direction> parameter.
        It also requires the <level_tile_map> and <crates> parameters, for collisions."""

        # We compute the next coordinates
        next_column = self.column + CHARACTER_DIRECTIONS[direction]['dx']
        next_row = self.row + CHARACTER_DIRECTIONS[direction]['dy']

        # We check for the collision with any other crate
        for crate in crates:
            if next_column == crate.column and next_row == crate.row:
                return False

        # We check if the next tile is an empty one, and return if the move succeeds
        if not level_tile_map[next_row][next_column]:
            # We change the coordinates of the crate
            self.change_coords(next_column, next_row, trophies)

            return True

        return False

class GameManager():
    """Class managing the game and its different components."""
    def __init__(self, screen):
        """Constructor method. It initializes the attributes of the class."""
        self.screen = screen # Represents the surface of the window
        self.background = BackgroundManager() # Background of the game
        self.character = Character(0, 0, 0) # Character
        self.crates = [] # Crates

        # Diferent rendering groups
        self.background_group = pygame.sprite.Group()
        self.character_group = pygame.sprite.Group()
        self.crates_group = pygame.sprite.Group()

        # We load the textures of the crates and the trophies
        Crate.load_textures()
        self.trophy_texture = load_background_texture(TROPHY)

        # Stack storing the moves of the character
        self.move_queue = collections.deque()

        # Initialization of the buttons available in-game
        self.back_to_menu_button = Button(
            WINDOW_SIZE[0] / 4 - GAME_BUTTONS_WIDTH / 2,
            WINDOW_SIZE[1] - GAME_BUTTONS_Y_MARGIN - GAME_BUTTONS_HEIGHT,
            GAME_BUTTONS_WIDTH,
            GAME_BUTTONS_HEIGHT,
            'Menu'
        )

        self.clear_button = Button(
            WINDOW_SIZE[0] / 2 - GAME_BUTTONS_WIDTH / 2,
            WINDOW_SIZE[1] - GAME_BUTTONS_Y_MARGIN - GAME_BUTTONS_HEIGHT,
            GAME_BUTTONS_WIDTH,
            GAME_BUTTONS_HEIGHT,
            'Refaire'
        )

        self.back_button = Button(
            3 * WINDOW_SIZE[0] / 4 - GAME_BUTTONS_WIDTH / 2,
            WINDOW_SIZE[1] - GAME_BUTTONS_Y_MARGIN - GAME_BUTTONS_HEIGHT,
            GAME_BUTTONS_WIDTH,
            GAME_BUTTONS_HEIGHT,
            'Annuler'
        )

    def parse(self, level_filename, character_id):
        """Method parsing a level file and consequently
        initializing the different components of the game"""

        # We try to parse the level
        if self.background.parse(level_filename):
            # We add the background to the rendering group
            self.background_group.add(self.background)

            # We initialize the character
            self.character = Character(
                self.background.initial_character_coords[0],
                self.background.initial_character_coords[1],
                character_id
            )

            # We add the character to the rendering group
            self.character_group.add(self.character)

            # Then we initialize the crates and add them to the rendering group
            for crate in self.background.initial_crates:
                self.crates.append(Crate(crate[0], crate[1]))
                self.crates_group.add(self.crates[-1])

        else:
            raise ValueError

    def mainloop(self):
        """The main loop of the game. It looks for the inputs
        of the user to move the elements of the game."""

        # List of the codes of the arrow keys
        arrow_keys = [pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT]

        while True:
            # Events processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # If an arrow key is pressed, then we move the character
                if event.type == pygame.KEYDOWN and event.key in arrow_keys:
                    self.character.update(
                        event.key,
                        self.background.background_map,
                        self.crates,
                        self.background.initial_trophies,
                        self.move_queue
                    )

                # If the mouse moves, we have to update the buttons
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()

                    self.back_to_menu_button.on_mouse_move(mouse_position[0], mouse_position[1])
                    self.clear_button.on_mouse_move(mouse_position[0], mouse_position[1])
                    self.back_button.on_mouse_move(mouse_position[0], mouse_position[1])

                # If the mouse is clicked, we have to check for all the buttons
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()

                    # If the user clicks on the 'back' button,
                    # we have to move the character accordingly.
                    if self.back_button.collides(mouse_position[0], mouse_position[1]):
                        if len(self.move_queue) > 0:
                            last_move = self.move_queue.pop()

                            self.character.update(
                                last_move[0],
                                self.background.background_map,
                                self.crates,
                                self.background.initial_trophies,
                                self.move_queue,
                                True,
                                last_move[1]
                            )

                    # If the user clicks on the 'clear' button,
                    # we restart the level as it was initially
                    elif self.clear_button.collides(mouse_position[0], mouse_position[1]):
                        # We clear the history of moves
                        self.move_queue.clear()

                        # We reset the crates to their initial positions
                        for index in range(len(self.crates)):
                            self.crates[index].change_coords(
                                self.background.initial_crates[index][0],
                                self.background.initial_crates[index][1],
                                self.background.initial_trophies
                            )

                        # Finally, we reset the position of the character
                        self.character.change_coords(
                            self.background.initial_character_coords[0],
                            self.background.initial_character_coords[1]
                        )

            # Drawing the different components of the game
            self.background_group.draw(self.screen)

            for trophy in self.background.initial_trophies:
                self.screen.blit(
                    self.trophy_texture,
                    (trophy[0] * TILE_SIZE, trophy[1] * TILE_SIZE)
                )

            self.crates_group.draw(self.screen)
            self.character_group.draw(self.screen)

            # Displaying the buttons at the bottom of the screen
            self.back_to_menu_button.draw(self.screen)
            self.clear_button.draw(self.screen)
            self.back_button.draw(self.screen)

            # Updating the screen
            pygame.display.flip()
