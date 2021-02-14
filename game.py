"""
This module contains the different classes
which manage the game itself.
"""

import sys
import pygame
from user_interface import Button
from constants import (BACKGROUND_TEXTURES_PATH, CRATE, TILE_SIZE, RED_CRATE,
                       TROPHY, WINDOW_SIZE, WINDOW_TILE_SIZE, CHARACTER, CHARACTERS_INFO,
                       CHARACTER_DIRECTIONS, GAME_BUTTONS_HEIGHT, GAME_BUTTONS_WIDTH,
                       GAME_BUTTONS_Y_MARGIN)

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

class BackgroundManager():
    """Class managing the background of the game."""
    def __init__(self):
        """Constructor method. It initializes the different attributes of the background."""

        # Initial coordinates of the character
        self.character_coords = ()

        # Lists of the initial coordinates of the crates and trophies on the map
        self.crates, self.trophies = [], []

        # List of lists containing the codes of the tiles of the map
        self.level_tile_map = []

        # Image of the background
        self.background_image = pygame.Surface(WINDOW_SIZE)

    def parse(self, filename):
        """Method parsing the background image from a level file."""

        # We reset the different attributes, so that the user can call this method multiple times
        self.crates, self.trophies, self.level_tile_map = [], [], []

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

                self.level_tile_map.append(tile_codes)

        # If an error occured, or if the number of lines is not valid, we return False
        if error or len(self.level_tile_map) != WINDOW_TILE_SIZE:
            return False

        # Now we create the background image from the <level_tile_map> variable
        for row in range(WINDOW_TILE_SIZE):
            for column in range(WINDOW_TILE_SIZE):
                # Variable containing the code of the tile we will finally display
                displayed_tile = 0

                # If the tile code corresponds to a crate or a trophy,
                # we do not want to add it to the background.
                # Instead, we store its coordinates for later use
                if self.level_tile_map[row][column] == CRATE:
                    self.crates.append((column, row))

                elif self.level_tile_map[row][column] == TROPHY:
                    self.trophies.append((column, row))

                elif self.level_tile_map[row][column] == CHARACTER:
                    self.character_coords = (column, row)

                else:
                    displayed_tile = self.level_tile_map[row][column]

                # We erase the crates, trophies, and character from the <level_tile_map> variable
                # (we have already stored their coordinates in other variables)
                self.level_tile_map[row][column] = displayed_tile

                # Coordinates of the tile in the background
                dest_coord = (column * TILE_SIZE, row * TILE_SIZE)

                # Rectangle defining the portion of the
                # background textures taken by the tile we want
                source_rect = pygame.Rect(TILE_SIZE * displayed_tile, 0, TILE_SIZE, TILE_SIZE)

                # Finally, we copy this portion of the textures in
                # the background image, at the computed coordinates
                self.background_image.blit(background_textures, dest_coord, source_rect)

        return True

    def draw(self, screen):
        """Method copying the background image onto the <screen> surface."""
        screen.blit(self.background_image, (0, 0))

class Character():
    """Class managing the character in the game"""
    def __init__(self, x, y, character_id):
        """Constructor mathod. It initializes the character depending on the given <character_id>"""

        # Coordinates of the character
        self.column, self.row = x, y

        # We retrieve the size of the character from the constants
        # thanks to the <character_id> parameter
        self.height = CHARACTERS_INFO[character_id]['height']
        self.width = CHARACTERS_INFO[character_id]['width']

        # Initial direction of the character
        self.direction = pygame.K_DOWN

        # Textures of the character
        self.textures = pygame.image.load(CHARACTERS_INFO[character_id]['textures_path'])
        self.textures.convert_alpha()

    def move(self, direction, level_tile_map, crates, trophies):
        """Method moving the character with the given <direction> parameter.
        It also requires the <level_tile_map>, <crates> and <trophies>
        parameters, for collisions."""

        # First, we set up the new direction
        self.direction = direction

        # Then we compute the next coordinates
        next_column = self.column + CHARACTER_DIRECTIONS[self.direction]['dx']
        next_row = self.row + CHARACTER_DIRECTIONS[self.direction]['dy']

        # Variable which saves if the collisions with the crates are not problematic
        collision_ok = True

        # We check for the collision with any crate
        for crate in crates:
            if crate.column == next_column and crate.row == next_row:
                collision_ok = crate.move(direction, level_tile_map, crates, trophies)

        # We check if the next tile is an empty one
        if not level_tile_map[next_row][next_column] and collision_ok:
            self.column, self.row = next_column, next_row

    def draw(self, screen):
        """Method copying the character image (depending on the <direction> variable)
        on the <screen> surface"""

        # Coordinates of the character on the screen
        dest_coords = (
            TILE_SIZE * self.column + (TILE_SIZE - self.width) // 2,
            TILE_SIZE * self.row + (TILE_SIZE - self.height) // 2
        )

        # Rectangle defining the portion of the textures that we will display
        source_rect = pygame.Rect(
            self.width * CHARACTER_DIRECTIONS[self.direction]['texture_pos'], 0,
            self.width, self.height
        )

        screen.blit(self.textures, dest_coords, source_rect)

class Crate():
    """Class managing a crate in the game."""

    @staticmethod
    def loadTextures():
        """Static method loading the textures of the crates (regular and red)"""
        Crate.regular_crate_texture = load_background_texture(CRATE)
        Crate.red_crate_texture = load_background_texture(RED_CRATE)

    def __init__(self, x, y):
        """Constructor method. It initializes the coordinates of the crate."""

        # Coordinates of the crate
        self.column, self.row = x, y

        # Variable which determines if the crate is red
        self.red = False

    def move(self, direction, level_tile_map, crates, trophies):
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
            # We edit the coordinates of the crate
            self.column, self.row = next_column, next_row

            # If the crate is on a trophy, then it becomes red
            self.red = (self.column, self.row) in trophies

            return True

        return False

    def draw(self, screen):
        """Method copying the crate texture at the right place
        on the map, depending on the coordinates and the <red> attribute
         of the instance."""

        screen.blit(
            Crate.red_crate_texture if self.red else Crate.regular_crate_texture,
            (self.column * TILE_SIZE, self.row * TILE_SIZE)
        )

class GameManager():
    """Class managing the game and its different components."""
    def __init__(self, screen):
        """Constructor method. It initializes the attributes of the class."""
        self.screen = screen # Represents the surface of the window
        self.background = BackgroundManager() # Background of the game
        self.character = Character(0, 0, 0) # Character
        self.crates = [] # Crates

        # We load the textures of the crates and the trophies
        Crate.loadTextures()
        self.trophy_texture = load_background_texture(TROPHY)

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
            # We initialize the character
            self.character = Character(
                self.background.character_coords[0],
                self.background.character_coords[1],
                character_id
            )

            # Then we initialize the crates
            for crate in self.background.crates:
                self.crates.append(Crate(crate[0], crate[1]))

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
                    self.character.move(
                        event.key,
                        self.background.level_tile_map,
                        self.crates,
                        self.background.trophies
                    )

                # If the mouse moves, we have to update the buttons
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()

                    self.back_to_menu_button.on_mouse_move(mouse_position[0], mouse_position[1])
                    self.clear_button.on_mouse_move(mouse_position[0], mouse_position[1])
                    self.back_button.on_mouse_move(mouse_position[0], mouse_position[1])

            # Drawing the different components of the game
            self.background.draw(self.screen)

            for trophy in self.background.trophies:
                self.screen.blit(
                    self.trophy_texture,
                    (trophy[0] * TILE_SIZE, trophy[1] * TILE_SIZE)
                )

            self.character.draw(self.screen)

            for crate in self.crates:
                crate.draw(self.screen)

            # Displaying the buttons at the bottom of the screen
            self.back_to_menu_button.draw(self.screen)
            self.clear_button.draw(self.screen)
            self.back_button.draw(self.screen)

            # Updating the screen
            pygame.display.flip()
